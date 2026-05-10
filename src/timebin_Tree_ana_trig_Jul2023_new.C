#include <sys/wait.h>

/*
class myTGraph : public TGraph {
  using TGraph::TGraph;
  public: 
  Double_t GetPointX(Int_t i) {if (i < 0 || i >= fNpoints || !fX) return -1.; return fX[i];};
  Double_t GetPointY(Int_t i) {if (i < 0 || i >= fNpoints || !fY) return -1.; return fY[i];};
  void SetPointX(Int_t i, Double_t x) {SetPoint(i, x, GetPointY(i));};
  void SetPointY(Int_t i, Double_t y) {SetPoint(i, GetPointX(i), y);};
};
*/

void timebin_Tree_ana_trig_Jul2023(Int_t ncpu, std::string datafiles, Int_t runNumber, Int_t evmax=0, std::string cond="1") {

  Int_t nch = 36;

  Double_t frequency = 100; // MHz

  Int_t nch_mask[36] = { 0,0,0,0,0,0,0,0,
                         1,1,1,1,1,1,0,1,
                         0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,
                         0,0,0,0};

  Int_t nch_plot[36] = { 0,0,0,0,0,0,0,0,
                         1,1,1,1,1,1,0,1,
                         0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,
                         0,0,0,0};

  Int_t nch_trig[36] = { 0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,
                         0,0,0,0,0,0,0,0,
                         0,0,0,0};

  Int_t nch_guard[36] = { 0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,1,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0,0,0,0,0,
                          0,0,0,0};

  TString chNames[36] = { "empty00", "empty01", "empty02","empty03","empty04","empty05","empty06","empty07",
                          "MCP1","MCP2","G4PZ","G5PZ","H4PZ","H5PZ","empty14","WAVE1BP",
                          "empty16","empty17","empty18","empty19","empty20","empty21","empty22","empty23",
                          "empty24","empty25","empty26","empty27","empty28","empty29","empty30","empty31",
                          "empty32","empty33","empty34","empty35"};


  Double_t fixmax[36] = { -1, -1, -1, -1, -1, -1, -1, -1,
                          -1, -1, -1, -1, -1, -1, -1, -1, 
                          -1, -1, -1, -1, -1, -1, -1, -1,
                          -1, -1, -1, -1, -1, -1, -1, -1,
                          -1, -1, -1, -1};

  Int_t polarity[36] = { 1,  1, 1,  1,  -1,  -1,  -1, 1,
                        -1, -1, 1,  1,   1,   1,  1, 1,
                         1, 1, 1, 1, 1, 1, 1, 1,
                         1,  1,  1,  1,  1,  1,  1, 1,
                         -1, -1, -1, -1 };

  Double_t cfd[10] = { 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 };

  Double_t flatrange[36] = { 20, 20, 20, 20, 20, 20, 20, 20,
                             20, 20, 20, 20, 20, 20, 20, 20,
                             20, 20, 20, 20, 20, 20, 20, 20,
                             20, 20, 20, 20, 20, 20, 20, 20,
                             20, 20, 20, 20 };


  Double_t maxfind[36] = { 600, 600, 600, 600, 600, 600, 600, 600,
                           600, 600, 600, 600, 600, 600, 600, 600,
                           400, 400, 400, 400, 400, 400, 400, 400,
                           400, 400, 400, 400, 400, 400, 400, 400,
                           900, 900, 900, 900 };
 
  Double_t drs4w[36] = { 204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8,
                         204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8,
                         204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8,
                         204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8, 204.8,
                         204.8, 204.8, 204.8, 204.8 };
 
  Int_t doPlot = 0;
  if(ncpu==0) doPlot = 1;

  std::string datadir="/storage/gpfs_data/local/lhcb/users/vagnoni/2023_july/spacal_w_LAPPD_DIG_SPS";

  Int_t nchild=0;

  Int_t frk=0;
  for(Int_t i=0; i<ncpu; ++i) {
    frk=fork();
    if(frk<0) {
       cout << "Error: cannot fork" << endl;
       exit(1);
    }
    if(!frk) break;
    ++nchild;
  }

  if(frk) {
    int status;
    while(waitpid(-1,&status,0)>0);

    TChain chain("T","T");
    for(Int_t i=0; i<ncpu; ++i) {
      chain.Add(Form("buffer/%stobemergedana_%d.root/tt",datafiles.c_str(),i));
    }

    cout << "Childs done. Merging files" << endl;

    chain.Merge("merged.root");
    chain.Merge(Form("%s/mergedana_%d.root",datadir.c_str(),runNumber));

    cout << "Done" << endl;

    exit(0);
  }

  if(ncpu==0) ncpu=1;

  TCanvas *c[36];

  struct {
    Double_t t[16][11];
    Double_t tdown[16][10];
    Double_t max[16];
    Double_t min[16];
    Double_t area[16];
    Double_t xwc[3];
    Double_t ywc[3];
    Double_t tmcp[11];
    Double_t tmcpd[11];
    Double_t maxmcp[2];
    Double_t ttrig[4];
    Double_t trun;
    Int_t imax[4];
    Int_t jmax[4];
    Int_t entry;
  } data;

  std::string branch="t[16][11]/D:tdown[16][10]/D:max[16]/D:min[16]/D:area[16]/D:xwc[3]/D:ywc[3]/D:tmcp[11]/D:tmcpd[11]/D:maxmcp[2]/D:ttrig[4]/D:trun/D:imax[4]/I:jmax[4]/I:entry/I";

  TTree *ttree = new TTree("tt","");
  ttree->Branch("data", &data.t[0][0], branch.c_str());

  TTree *ttreehelp = new TTree("thelp","");
  ttreehelp->Branch("data", &data.t[0][0], branch.c_str());

  TF1 *func=new TF1("func","gaus+[3]",-5000,5000);

  std::string fcal[nch];
  std::string fcals[nch];
  std::string ftimes[nch];

  for(Int_t j=0; j<nch; j++) {
    if(!nch_mask[j] || nch_trig[j]) continue;
    fcal[j] = Form("calib_Bologna/calib_cell_%d.txt",j);
    fcals[j] = Form("calib_Bologna/calib_sample_%d.txt",j);
    ftimes[j] = Form("calib_Bologna/calib_time_%d.txt",j); 
  }

  FILE *fdcal[nch];
  FILE *fdcals[nch];
  FILE *fdtimes[nch];
  for(Int_t j=0; j<nch; j++) {
    if(!nch_mask[j] || nch_trig[j]) continue;
    fdcal[j]=fopen(fcal[j].c_str(),"r");
    fdcals[j]=fopen(fcals[j].c_str(),"r");
    fdtimes[j]=fopen(ftimes[j].c_str(),"r");
  }

  //if(doPlot) for(Int_t i=0; i<nch; ++i) if(nch_mask[i] && !nch_trig[i]) c[i] = new TCanvas();
  if(doPlot) for(Int_t i=0; i<nch; ++i) if(nch_mask[i]) c[i] = new TCanvas();

  TGraph *hg[nch];

  for(Int_t i=0; i<nch; ++i) {
    if(!nch_mask[i]) continue;
    hg[i] = new TGraph(1024);
    hg[i]->SetName(Form("hg%d",i));
    hg[i]->SetMarkerStyle(20);
    hg[i]->SetMarkerSize(0.5); 
  }

  Double_t p0[nch][1024];
  Double_t p1[nch][1024];
  Double_t p2[nch][1024];

  Double_t pa0[nch][1024];
  Double_t pa1[nch][1024];
  Double_t pa2[nch][1024];

  Double_t timev[nch][1024];

  for(Int_t j=0; j<nch; ++j) {
    if(nch_mask[j] && nch_trig[j]) {
      for(Int_t i=0; i<1024; ++i) {
        p0[j][i] = 0; p1[j][i] = 1/4096.; p2[j][i] = 0;
        pa0[j][i] = 0; pa1[j][i] = 1; pa2[j][i] = 0;
        timev[j][i] = drs4w[j]/1024.;
      }
    } else if(nch_mask[j]) {
      for(Int_t i=0; i<1024; ++i) {
        fscanf(fdcal[j],"%lg %lg %lg", &p0[j][i], &p1[j][i], &p2[j][i]);
        fscanf(fdcals[j],"%lg %lg %lg", &pa0[j][i], &pa1[j][i], &pa2[j][i]);
        fscanf(fdtimes[j],"%lg", &timev[j][i]);
      }
    }
  }

  // Variables to read the data
  Int_t startcell[nch];
  Float_t fbuf[nch][1024];
  Int_t pattern = 0;
  Double_t dwc_x1 = 0, dwc_x2 = 0, dwc_x3 = 0,
           dwc_y1 = 0, dwc_y2 = 0, dwc_y3 = 0,
           trun = 0;
  TChain * inChain = new TChain("DATA","DATA");
  inChain->Add(Form("%s/%s_%02d.root/DATA",datadir.c_str(),datafiles.c_str(),runNumber));
  auto listOfBranches = inChain->GetListOfBranches();
  if(!nchild) printf("READING FILE %s/%s_%02d.root WITH %lld ENTRIES\n",datadir.c_str(),datafiles.c_str(),runNumber,inChain->GetEntries());

  inChain->SetBranchStatus("*",0);
  inChain->SetBranchStatus("pattern",1);
  inChain->SetBranchStatus("t",1);
  inChain->SetBranchStatus("x1",1);
  inChain->SetBranchStatus("x2",1);
  inChain->SetBranchStatus("x3",1);
  inChain->SetBranchStatus("y1",1);
  inChain->SetBranchStatus("y2",1);
  inChain->SetBranchStatus("y3",1);
  inChain->SetBranchAddress("pattern",&pattern);
  inChain->SetBranchAddress("t",&trun);
  inChain->SetBranchAddress("x1",&dwc_x1);
  inChain->SetBranchAddress("x2",&dwc_x2);
  inChain->SetBranchAddress("x3",&dwc_x3);
  inChain->SetBranchAddress("y1",&dwc_y1);
  inChain->SetBranchAddress("y2",&dwc_y2);
  inChain->SetBranchAddress("y3",&dwc_y3);
  for(Int_t j=0; j<nch; j++) {
    if(!nch_mask[j]) continue;
    inChain->SetBranchStatus(Form("%s_*",chNames[j].Data()),1);
    if(listOfBranches->FindObject(Form("%s_stcell%02d",chNames[j].Data(),j))==NULL) {
      nch_mask[j] = 0;
      continue;
    }
    if(!nchild) printf("ADDING BRANCH %s_stcell%02d\n",chNames[j].Data(),j);
    inChain->SetBranchAddress(Form("%s_stcell%02d",chNames[j].Data(),j),&startcell[j]);
    inChain->SetBranchAddress(Form("%s_ad%02d",chNames[j].Data(),j),fbuf[j]);
  }

  Int_t n=0;
  for(Int_t iEntry = nchild, nEntries = inChain->GetEntries(); 
      iEntry < nEntries; iEntry += ncpu) {

    inChain->GetEntry(iEntry);
    data.entry = iEntry;
    data.trun = trun;
    if(pattern!=4) continue;
    if(!(n%200)) printf("CHILD %d READING EVENT %d ENTRY %d/%d\n",nchild,n+1,iEntry,nEntries);
    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j]) continue;
      Double_t tinc=0;

      for(Int_t i=0; i<1024; ++i) {
        Int_t index = (i+startcell[j])%1024;
        Double_t v = p0[j][index]+p1[j][index]*(fbuf[j][i]-p2[j][index]);
        v = pa0[j][i]+pa1[j][i]*(v-pa2[j][i]);
        hg[j]->SetPoint(i,tinc,v*polarity[j]);
        tinc += timev[j][index];
      }
    }

    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j]) continue;
      Double_t t0;
      Int_t index = (1024-startcell[j])%1024;
      if     (j<8)   t0 = hg[7]->GetPointX(index);
      else if(j<16)  t0 = hg[15]->GetPointX(index);
      else if(j<24)  t0 = hg[23]->GetPointX(index);
      else if(j<32)  t0 = hg[31]->GetPointX(index);
      else if(j==32) t0 = hg[7]->GetPointX(index);
      else if(j==33) t0 = hg[15]->GetPointX(index);
      else if(j==34) t0 = hg[23]->GetPointX(index);
      else if(j==35) t0 = hg[31]->GetPointX(index);

      Double_t tch0 = hg[j]->GetPointX(index);
      for(Int_t i=0; i<1024; ++i) {
        hg[j]->SetPoint(i,hg[j]->GetPointX(i)-(tch0-t0),hg[j]->GetPointY(i));
      }
    }

    Double_t max[nch];
    Double_t min[nch];
    Double_t xMin[nch][10];
    Double_t xMax[nch][10];

    Double_t yMin[nch][10];
    Double_t yMax[nch][10];

    Double_t xMinDown[nch][10];
    Double_t xMaxDown[nch][10];

    Double_t yMinDown[nch][10];
    Double_t yMaxDown[nch][10];

    Double_t zero[nch];

    Double_t area[nch];
    memset(area,0,nch*sizeof(Double_t));

    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j]) continue;

      Int_t chg;
      if     (j<8)   chg=7;
      else if(j<16)  chg=15;
      else if(j<24)  chg=23;
      else if(j<32)  chg=31;
      else if(j==32) chg=7;
      else if(j==33) chg=15;
      else if(j==34) chg=23;
      else if(j==35) chg=31;

      Int_t probs[1024];
      memset(probs,0,1024*sizeof(Int_t));
      for(Int_t i=5; i<970; ++i) {
        Double_t ym1=(hg[chg]->GetPointY(i+1)-hg[chg]->GetPointY(i))/(hg[chg]->GetPointX(i+1)-hg[chg]->GetPointX(i))*(hg[chg]->GetPointX(i-1)-hg[chg]->GetPointX(i)) + hg[chg]->GetPointY(i);
        Double_t yp2=(hg[chg]->GetPointY(i+1)-hg[chg]->GetPointY(i))/(hg[chg]->GetPointX(i+1)-hg[chg]->GetPointX(i))*(hg[chg]->GetPointX(i+2)-hg[chg]->GetPointX(i)) + hg[chg]->GetPointY(i);

        if(hg[chg]->GetPointY(i-1) - ym1>0.005 && hg[chg]->GetPointY(i+2) - yp2>0.005) {
          probs[i]=1;
          probs[i+1]=1;
        }

      }

      Int_t pr[1024];
      memcpy(pr,probs,1024*sizeof(Int_t));

      if(pr[0]) {
        Int_t m;
        for(m=1; m<1024; ++m) if(!pr[m]) break;
        if(m==1024) { cout << "Impossible... exiting" << endl; exit(1); }
        hg[j]->SetPointY(0,hg[j]->GetPointY(m));
        pr[0]=0;
      }

      if(pr[1023]) {
        Int_t m;
        for(m=1022; m>=0; --m) if(!pr[m]) break;
        if(m==-1) { cout << "Impossible... exiting" << endl; exit(1); }
        hg[j]->SetPointY(1023,hg[j]->GetPointY(m));
        pr[1023]=0;
      }

      for(Int_t i=1; i<1023; ++i) {
        if(pr[i]) {
          Int_t mu, md;
          for(mu=i+1; mu<1024; ++mu) if(!pr[mu]) break;
          for(md=i-1; md<1024; --md) if(!pr[md]) break;
          Double_t diff = hg[j]->GetPointY(mu)-hg[j]->GetPointY(md);

          Double_t diffX = hg[j]->GetPointX(mu)-hg[j]->GetPointX(md);
          Double_t diffY = hg[j]->GetPointY(mu)-hg[j]->GetPointY(md);

          hg[j]->SetPointY(i,diffY/diffX*(hg[j]->GetPointX(i)-hg[j]->GetPointX(md))+hg[j]->GetPointY(md));
          pr[i]=0;
        }
      }
    }

    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j] || !nch_trig[j]) continue;
      hg[j]->Fit("pol0", "0Q", "", 5, flatrange[j]);
      TF1 *fit = hg[j]->GetFunction("pol0");
      zero[j] = fit->GetParameter(0);
      Int_t i;
      max[j] = TMath::MaxElement(maxfind[j],&(hg[j]->GetY()[5]))-zero[j];
      min[j] = TMath::MinElement(maxfind[j],&(hg[j]->GetY()[5]))-zero[j];
      if(fixmax[j]>0) max[j]=fixmax[j];

      for(Int_t icfd=0; icfd<10; ++icfd) {
        for(xMax[j][icfd] = 0, i = 1; i < 1024; ++i) {
          if(hg[j]->GetPointY(i)-zero[j] > cfd[icfd]*max[j]) {
            xMax[j][icfd] = hg[j]->GetPointX(i);
            yMax[j][icfd] = hg[j]->GetPointY(i);
            break;
          }
        }

        for(xMin[j][icfd] = drs4w[j]; i > 0; --i) {
          if(hg[j]->GetPointY(i)-zero[j] < cfd[icfd]*max[j]) {
            xMin[j][icfd] = hg[j]->GetPointX(i);
            yMin[j][icfd] = hg[j]->GetPointY(i);
            break;
          }
        }
      }
    }

    Double_t t[nch][11];
    Double_t tdown[nch][10];

    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j] || !nch_trig[j]) continue;
      for(Int_t icfd=0; icfd<10; ++icfd) {
        Double_t p1 = (yMax[j][icfd]-yMin[j][icfd])/(xMax[j][icfd]-xMin[j][icfd]);
        Double_t p0 = yMin[j][icfd] - p1*xMin[j][icfd];
        t[j][icfd] = (cfd[icfd]*max[j]+zero[j]-p0)/p1;
      }
    }

    Double_t zeror[nch][100];
    memset(zeror,0,nch*100*sizeof(Int_t));
    Int_t nzeror[nch];
    memset(nzeror,0,nch*sizeof(Int_t));

    Double_t zerof[nch][100];
    memset(zerof,0,nch*100*sizeof(Int_t));
    Int_t nzerof[nch];
    memset(nzerof,0,nch*sizeof(Int_t));

    Double_t timez=0;
    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j]) continue;
      for(Int_t k = 0; k < 1024; ++k) {
          if(j<8) continue;
          else if(j<16) continue;  
//          else if(j<16) hg[j]->SetPointX(k,hg[j]->GetPointX(k)-t[33][5]+t[32][5]);
          else if(j<24) hg[j]->SetPointX(k,hg[j]->GetPointX(k)-t[34][5]+t[32][5]);
          else if(j<32) hg[j]->SetPointX(k,hg[j]->GetPointX(k)-t[35][5]+t[32][5]);
          else if(j==32) continue;
          else if(j==33) hg[j]->SetPointX(k,hg[j]->GetPointX(k)-t[33][5]+t[32][5]);
          else if(j==34) hg[j]->SetPointX(k,hg[j]->GetPointX(k)-t[34][5]+t[32][5]);
          else if(j==35) hg[j]->SetPointX(k,hg[j]->GetPointX(k)-t[35][5]+t[32][5]);
      }

      if(hg[j]->GetPointX(0)>timez) timez=hg[j]->GetPointX(0);

    }

    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j] || !nch_guard[j]) continue;

      Double_t thr=0.5*(TMath::MaxElement(965,&(hg[j]->GetY()[5]))+TMath::MinElement(970,&(hg[j]->GetY()[5])));

      Double_t oldV = hg[j]->GetPointY(4);
      for(Int_t i=5; i<970; ++i) {
        Double_t newV = hg[j]->GetPointY(i);
        if(newV>thr&&oldV<thr) {
           zeror[j][nzeror[j]]=hg[j]->GetPointX(i-1)-(oldV-thr)*(hg[j]->GetPointX(i)-hg[j]->GetPointX(i-1))/(newV-oldV);
           ++nzeror[j];
        }
        oldV=newV;
      }

      oldV = hg[j]->GetPointY(4);
      for(Int_t i=5; i<970; ++i) {
        Double_t newV = hg[j]->GetPointY(i);
        if(newV<thr&&oldV>thr) {
           zerof[j][nzerof[j]]=hg[j]->GetPointX(i-1)-(oldV-thr)*(hg[j]->GetPointX(i)-hg[j]->GetPointX(i-1))/(newV-oldV);
           ++nzerof[j];
        }
        oldV=newV;
      }
    }

    for(Int_t j=15; j<nch; ++j) {
      if(!nch_mask[j] || !nch_guard[j] ) continue;
      Double_t diffr=0;
      Int_t cntr=0;
      if(fabs(zeror[j][0]-zeror[15][0])<500/frequency) {
        for(Int_t l=0; l<nzeror[j] && l<nzeror[15]; ++l) {
          diffr+=zeror[j][l]-zeror[15][l];
          ++cntr;
        }
      } else if (fabs(zeror[j][1]-zeror[15][0])<500/frequency) {
        for(Int_t l=0; l<nzeror[j]-1 && l<nzeror[15]; ++l) {
          diffr+=zeror[j][l+1]-zeror[15][l];
          ++cntr;
        }
      } else {
        for(Int_t l=0; l<nzeror[j] && l<nzeror[15]-1; ++l) {
          diffr+=zeror[j][l]-zeror[15][l+1];
          ++cntr;
        }
      }
      diffr/=cntr;

      Double_t difff=0;
      Int_t cntf=0;
      if(fabs(zerof[j][0]-zerof[15][0])<500/frequency) {
        for(Int_t l=0; l<nzerof[j] && l<nzerof[15]; ++l) {
          difff+=zerof[j][l]-zerof[15][l];
          ++cntf;
        }
      } else if (fabs(zerof[j][1]-zerof[15][0])<500/frequency) {
        for(Int_t l=0; l<nzerof[j]-1 && l<nzerof[15]; ++l) {
          difff+=zerof[j][l+1]-zerof[15][l];
          ++cntf;
        }
      } else {
        for(Int_t l=0; l<nzerof[j] && l<nzerof[15]-1; ++l) {
          difff+=zerof[j][l]-zerof[15][l+1];
          ++cntf;
        }
      }
      difff/=cntf;

      Double_t diff=0.5*(diffr+difff);

      for(Int_t k=j-7; k<=j; ++k) {
        if(!nch_mask[k]) continue;
        for(Int_t i=0; i<1024; ++i) {
          hg[k]->SetPointX(i,hg[k]->GetPointX(i)-diff);
        }
      }
    }

    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j]) continue;
      hg[j]->Fit("pol0", "0Q", "", 5, flatrange[j]);
      TF1 *fit = hg[j]->GetFunction("pol0");
      zero[j] = fit->GetParameter(0);

      Int_t i;
      max[j] = TMath::MaxElement(maxfind[j],&(hg[j]->GetY()[5]))-zero[j];
      min[j] = TMath::MinElement(maxfind[j],&(hg[j]->GetY()[5]))-zero[j];
      if(fixmax[j]>0) max[j]=fixmax[j];

      for(Int_t icfd=0; icfd<10; ++icfd) {
        for(xMax[j][icfd] = 0, i = 1; i < 1024; ++i) {
          if(hg[j]->GetPointY(i)-zero[j] > cfd[icfd]*max[j]) {
            xMax[j][icfd] = hg[j]->GetPointX(i);
            yMax[j][icfd] = hg[j]->GetPointY(i);
            break;
          }
        }

        for(xMin[j][icfd] = drs4w[j]; i > 0; --i) {
          if(hg[j]->GetPointY(i)-zero[j] < cfd[icfd]*max[j]) {
            xMin[j][icfd] = hg[j]->GetPointX(i);
            yMin[j][icfd] = hg[j]->GetPointY(i);
            break;
          }
        }

        for(xMaxDown[j][icfd] = 0, i = 1023; i > 0; --i) {
          if(hg[j]->GetPointY(i)-zero[j] > cfd[icfd]*max[j]) {
            xMaxDown[j][icfd] = hg[j]->GetPointX(i);
            yMaxDown[j][icfd] = hg[j]->GetPointY(i);
            break;
          }
        }
        for(xMinDown[j][icfd] = drs4w[j]; i < 1024; ++i) {
          if(hg[j]->GetPointY(i)-zero[j] < cfd[icfd]*max[j]) {
            xMinDown[j][icfd] = hg[j]->GetPointX(i);
            yMinDown[j][icfd] = hg[j]->GetPointY(i);
            break;
          }
        }
      }

      for(Int_t i=5; i<maxfind[j]; ++i) {
        area[j]+=(hg[j]->GetPointY(i)-zero[j])*(hg[j]->GetPointX(i+1)-hg[j]->GetPointX(i));
      }

    }

    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j]) continue;
      for(Int_t icfd=0; icfd<10; ++icfd) {
        Double_t p1 = (yMax[j][icfd]-yMin[j][icfd])/(xMax[j][icfd]-xMin[j][icfd]);
        Double_t p0 = yMin[j][icfd] - p1*xMin[j][icfd];
        t[j][icfd] = (cfd[icfd]*max[j]+zero[j]-p0)/p1;

        p1 = (yMaxDown[j][icfd]-yMinDown[j][icfd])/(xMaxDown[j][icfd]-xMinDown[j][icfd]);
        p0 = yMinDown[j][icfd] - p1*xMinDown[j][icfd];
        tdown[j][icfd] = (cfd[icfd]*max[j]+zero[j]-p0)/p1;

      }
    }

    // Time of Maximum
    for(Int_t j=0; j<nch; ++j) {
      if(!nch_mask[j]) continue;
      Int_t idxtmp = TMath::LocMax(maxfind[j],&(hg[j]->GetY()[5]))+5;
      Double_t x1 = hg[j]->GetX()[idxtmp];
      Double_t x2 = hg[j]->GetX()[idxtmp-1];
      Double_t x3 = hg[j]->GetX()[idxtmp+1];
      Double_t y1 = hg[j]->GetY()[idxtmp];
      Double_t y2 = hg[j]->GetY()[idxtmp-1];
      Double_t y3 = hg[j]->GetY()[idxtmp+1];

      Double_t denom = (x1 - x2) * (x1 - x3) * (x2 - x3);
      Double_t A     = (x3 * (y2 - y1) + x2 * (y1 - y3) + x1 * (y3 - y2)) / denom;
      Double_t B     = (x3*x3 * (y1 - y2) + x2*x2 * (y3 - y1) + x1*x1 * (y2 - y3)) / denom;
      Double_t C     = (x2 * x3 * (x2 - x3) * y1 + x3 * x1 * (x3 - x1) * y2 + x1 * x2 * (x1 - x2) * y3) / denom;

      t[j][10] = -B / (2*A);
      Double_t yv = yv = C - B*B / (4*A);
      //if(j==2) printf("STICA %d %g\n",j,t[j][10]);
    }
    
    for(Int_t k=0; k<nch; ++k) {
      if(!nch_mask[k] || nch_trig[k] || nch_guard[k]) continue;
      for(Int_t icfd=0; icfd<10; ++icfd) {
        data.t[k][icfd]=t[k][icfd];
        data.tdown[k][icfd]=tdown[k][icfd];
      }
      data.t[k][10]=t[k][10];

      data.max[k]=max[k];
      data.min[k]=min[k];
      data.area[k]=area[k];
      //data.imax[k]=-1;
    }

    // Adding trigger time
    for(Int_t k=0; k<4; ++k) {
      if(!(nch_mask[k+32] && nch_trig[k+32])) continue;
      data.ttrig[k] = t[k+32][5];
    }

    // ORDER 4 LAPPD CHANNELS WITHIN SPACAL
    for(Int_t h=0; h<4; ++h) data.imax[h]=-1;
    for(Int_t h=0; h<4; ++h) {
      Double_t mh=-1;
      Int_t ih=-1;
      for(Int_t k=0; k<4; ++k) {
         if(data.imax[k]!=-1) continue;
         if(data.max[k]>mh) {
           ih=k;
           mh=data.max[k];
         }
       }
       data.imax[ih]=h;
       data.jmax[h]=ih;
    }
 
    data.xwc[0]=dwc_x1; data.xwc[1]=dwc_x2; data.xwc[2]=dwc_x3;
    data.ywc[0]=dwc_y1; data.ywc[1]=dwc_y2; data.ywc[2]=dwc_y3;

    for(Int_t icfd=0; icfd<11; ++icfd) {
      data.tmcp[icfd]=0.5*(t[8][icfd]+t[9][icfd]);
      data.tmcpd[icfd]=t[8][icfd]-t[9][icfd];
    }
    data.maxmcp[0] = max[8];
    data.maxmcp[1] = max[9];

    ++n;
    ttreehelp->Fill();
    if(ttreehelp->GetEntries(Form("%s%s",Form("Entry$==%d&&",n-1),cond.c_str()))==0) continue;


    if(doPlot) {
      Int_t lastk;
      for(Int_t k=0; k<nch; ++k) {
        if(!nch_mask[k] || nch_trig[k] || !nch_plot[k]) continue;
        lastk=k;
        c[k]->cd();
        hg[k]->Draw("AP");
        c[k]->Update();
      }
      c[lastk]->WaitPrimitive();
    }

    ttree->Fill();
  }

  //out:

  TFile *outfile=TFile::Open(Form("buffer/%stobemergedana_%d.root",datafiles.c_str(),nchild),"RECREATE");
  outfile->WriteTObject(ttree,"","Overwrite");
  outfile->Close(); 

  exit(0);

}

