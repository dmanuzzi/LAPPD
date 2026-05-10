#include <iostream>
#include <fstream>
#include <vector>
#include <map>
#include <algorithm>
#include <utility>

#include "TString.h"
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TF1.h"
#include "TLine.h"
#include "TStyle.h"
#include "TROOT.h"
#include "TH2D.h"
#include "TChain.h"
using namespace std;

struct Data{
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
};
inline Bool_t sel_mcp(Data &d, Double_t minmcp=0.05, Double_t maxmcp=0.85){
    if (d.maxmcp[0]<minmcp) return false;
    if (d.maxmcp[1]<minmcp) return false;
    if (d.maxmcp[0]>maxmcp) return false;
    if (d.maxmcp[1]>maxmcp) return false;
    return true;
}

pair<Double_t, Double_t> getBeamSpotCenter(Int_t run){
    if (run == 0 || run == 16 || run == 23 || run == 25 || run == 26 || run == 27 || run == 28 || run == 29 || run == 30 || run == 31 || run == 32 || run == 33 || run == 34 || run == 35 || run == 36 || run == 37 || run == 38 || run == 39 || run == 40 || run == 54 || run == 78 || run == 80 || run == 63 || run == 79)
        return make_pair( +3.7, -9.5);
    if (run == 1 || run == 17 || run == 41 || run == 53 || run == 73 || run == 64 || run == 86)
        return make_pair( +3.7, +3.0);
    if (run == 3 || run == 15 || run == 42 || run == 55 || run == 77 || run == 62 || run == 82)
        return make_pair( +3.7, -22.0);
    if (run == 4 || run == 20 || run == 43 || run == 56 || run == 76 || run == 61 || run == 90)
        return make_pair( +16.2, -22.0);
    if (run == 7 || run == 18 || run == 45 || run == 58 || run == 74 || run == 59 || run == 88)
        return make_pair( +16.2, +3.0);
    if (run == 8 || run == 19 || run == 44 || run == 57 || run == 75 || run == 60 || run == 89)
        return make_pair( +16.2, -9.5);
    if (run == 9 || run == 13 || run == 47 || run == 50 || run == 71 || run == 68 || run == 84)
        return make_pair( -8.8,  -9.5);
    if (run == 10 || run == 14 || run == 48 || run == 49 || run == 70 || run == 69 || run == 83)
        return make_pair( -8.8,  -22.0);
    if (run == 11 || run == 12 || run == 46 || run == 52 || run == 72 || run == 67 || run == 85)
        return make_pair( -8.8,  +3.0);
    printf("Unknown run, THIS SHOULD NOT HAPPEN!!!\n");
    return make_pair(0, 0);
}

inline Bool_t sel_geom(Data &d, Double_t& x_hat, Double_t& y_hat){
    if (abs(d.xwc[2]-d.xwc[1]+0.2)>1) return false;
    if (abs(d.ywc[2]-d.ywc[1]-1.5)>1.5) return false;
    if (d.xwc[2]<-21.3) return false;
    if (d.xwc[2]>28.7) return false; 
    if (d.ywc[2]<-34.5) return false;
    if (d.ywc[2]>15.5) return false;
    return (d.xwc[2] - x_hat) * (d.xwc[2] - x_hat) + (d.ywc[2] - y_hat) * (d.ywc[2] - y_hat) < 7.0 * 7.0;
}

int getEff(Int_t run_energy, TString nfout="output_getEff", 
           TString datadir = "/storage/gpfs_data/local/lhcb/users/vagnoni/2022_december"){

    map<TString, vector<Int_t>> energy_runs = {
        {"5.0",  { 48, 47, 46, 41, 45, 44, 43, 42, 40} },
        {"4.0",  { 70, 71, 72, 73, 74, 75, 76, 77, 78} },
        {"3.0",  { 49, 50, 52, 53, 58, 57, 56, 55, 54} },
        {"2.0",  { 83, 84, 85, 86, 88, 89, 90, 82, 79} },
        {"1.0",  { 69, 68, 67, 64, 59, 60, 61, 62, 63} },
        {"5.8", {80}}
    };
    vector<Int_t> runs;
    TString energy = "All", run = "All";
    if (run_energy<0){
        energy = Form("%.1f", -(float)run_energy);
        runs = energy_runs[energy];
    } else {
        run = Form("%d", run_energy); 
        runs.push_back(run.Atoi()); 
    }
        
    TChain *tin = new TChain("T", "T");
    vector<Int_t> run_seq;
    for (auto tmprun : runs){
        run_seq.push_back(tmprun);
        tin->Add(datadir + Form("/mergedana_%d.root", tmprun));
    }
    //TFile *fin = new TFile(datadir+Form("/mergedana_%d.root", run), "READ");
    // fin->ls();
    // TTree *tin = (TTree*)fin->Get("T");
    // tin->Print();
    Data event;
    tin->SetBranchAddress("data", &event);
    Int_t nentries = tin->GetEntries();
    Int_t nentries_selected = 0;
    vector<TH1D*> h_resT, h_resT_check,  h_max;
    vector<vector<TH1D*>> hh_max;
    vector<Float_t> Nsigmas = {1.,2.,3.,5.,20,50};
    Int_t nch = 4;
    vector<vector<Int_t>> nentries_Nsigma(nch, vector<Int_t>(Nsigmas.size(), 0));

    // Building some histograms
    for (Int_t i=0; i<nch; ++i){
        TString tmpTag = Form("run%s_E%s_ch%d",run.Data(),energy.Data(),i);
        TString title_resT = Form("h_resT_%s; t[%d][5]-tmcp[3] (ns); Candidates", tmpTag.Data(), i);
        h_resT.push_back(new TH1D("h_resT_" + tmpTag, title_resT, 100, -6.5, -4));
        h_resT_check.push_back(new TH1D("h_resT_check_" + tmpTag, "check_"+title_resT, 100, -6.0, -4.6));
        TString title_max = Form("h_max_%s; max[%d]; Candidates", tmpTag.Data(), i);
        h_max.push_back(new TH1D("h_max_" + tmpTag, title_max, 150, 0, 1));
        hh_max.emplace_back();
        for (auto Nsigma : Nsigmas){
            TString tmpTag_hh_max = Form("%s_%.0frms", tmpTag.Data(), Nsigma);
            TString title_hh_max = Form("hh_max_%s; max[%d]; Candidates", tmpTag_hh_max.Data(),i);
            hh_max.back().push_back(new TH1D("hh_max_"+tmpTag_hh_max, title_hh_max, 100, 0, 0.1));
        }
    }

    pair<Double_t, Double_t> beamSpotCenter;
    Double_t beamSpotCenter_x, beamSpotCenter_y;
    // Get reference resolution
    for (Int_t ientry = 0; ientry < nentries; ++ientry)
    {
        tin->GetEntry(ientry);
        Int_t tmprun = run_seq[tin->GetTreeNumber()];
        beamSpotCenter = getBeamSpotCenter(tmprun);
        beamSpotCenter_x = beamSpotCenter.first;
        beamSpotCenter_y = beamSpotCenter.second;

        if (!sel_geom(event, beamSpotCenter_x, beamSpotCenter_y))
            continue;
        if (!sel_mcp(event)) continue;
        for (Int_t i = 0; i < nch; ++i){
            if (event.max[i]<0.05) continue;
            if (event.max[i]>0.85) continue;
            h_resT_check[i]->Fill(event.t[i][5]-event.tmcp[3]);
        }
    }

    vector<Float_t> mean_resT_check, sigma_resT_check;
    vector<TCanvas*> c;
    gStyle->SetOptFit(1);
    for_each(h_resT_check.begin(), h_resT_check.end(), [&mean_resT_check, &sigma_resT_check, &c](TH1D *h) {
        TString ncanv = Form("c_%s", h->GetName());
        c.push_back(new TCanvas(ncanv, ncanv));
        c.back()->cd();
        h->Draw();
        h->Fit("gaus", "0");
        TF1* tmpf = h->GetFunction("gaus");
        tmpf->Draw("lsame");
        mean_resT_check.push_back(tmpf->GetParameter(1));
        sigma_resT_check.push_back(tmpf->GetParameter(2));
        c.back()->SaveAs(TString(c.back()->GetName()).ReplaceAll(".", "-") + ".pdf");
    });
    TFile *fout = new TFile(nfout+".root", "RECREATE");
    ofstream myfile;
    myfile.open(nfout + ".txt");
    for_each(c.begin(), c.end(), [fout](TCanvas *cc)
             { fout->WriteTObject(cc, cc->GetName()); });
    for (Int_t i=0; i<nch; ++i){
        printf("ch: %d; mean_check: %.4f ns; sigma_check: %.4f\n", i, mean_resT_check[i], sigma_resT_check[i]);
        myfile << Form("%d %.6f %.6f\n", i, mean_resT_check[i], sigma_resT_check[i]);
    }

    vector<TH1D*> h_resT_zoom;
    for (Int_t i=0; i<nch; ++i){
        TString tmpTag = Form("run%s_E%s_ch%d_zoom",run.Data(),energy.Data(),i);
        TString title_resT = Form("h_resT_%s; t[%d][5]-tmcp[3] (ns); Candidates", tmpTag.Data(), i);
        Double_t tmp_min = mean_resT_check[i] - 10.0 * sigma_resT_check[i];
        Double_t tmp_max = mean_resT_check[i] + 10.0 * sigma_resT_check[i];
        h_resT_zoom.push_back(new TH1D("h_resT_" + tmpTag, title_resT, 100, tmp_min, tmp_max));
    }
    //Get efficiency and plots
    TString name_h_xywc = Form("h_xywc_run%s_E%s", run.Data(),energy.Data());
    TH2D *h_xywc = new TH2D(name_h_xywc, name_h_xywc + "; x (mm); y (mm)", 75, -21.3, 28.7, 75, -34.5, 15.5);

    for (Int_t ientry=0; ientry<nentries; ++ientry){
        tin->GetEntry(ientry);
        Int_t tmprun = run_seq[tin->GetTreeNumber()];
        beamSpotCenter = getBeamSpotCenter(tmprun);
        beamSpotCenter_x = beamSpotCenter.first;
        beamSpotCenter_y = beamSpotCenter.second;

        if (!sel_geom(event, beamSpotCenter_x, beamSpotCenter_y)) continue;
        if (!sel_mcp(event)) continue;
        ++nentries_selected;
        h_xywc->Fill(event.xwc[2], event.ywc[2]);

        for (Int_t i = 0; i < nch; ++i){
            Double_t dt = event.t[i][5] - event.tmcp[3];
            h_resT[i]->Fill(dt);
            h_resT_zoom[i]->Fill(dt);
            h_max[i]->Fill(event.max[i]);
            for (Int_t j=0; j<(Int_t)Nsigmas.size(); ++j){
                if (dt < mean_resT_check[i] - Nsigmas[j] * sigma_resT_check[i])
                    continue;
                if (dt > mean_resT_check[i] + Nsigmas[j] * sigma_resT_check[i])
                    continue;
                nentries_Nsigma[i][j] += 1;
                hh_max[i][j]->Fill(event.max[i]);
            }
        }
    }

    for (Int_t i = 0; i < nch; ++i) {
        c.back()->SaveAs(TString(c.back()->GetName()).ReplaceAll(".", "-") + ".pdf");
        fout->WriteTObject(c.back(), c.back()->GetName());
        TString ncanv_zoom = Form("c_%s_zoom", h_resT_zoom[i]->GetName());
        c.push_back(new TCanvas(ncanv_zoom, ncanv_zoom));
        c.back()->cd();
        h_resT_zoom[i]->Draw("hist");
        h_resT_zoom[i]->Fit("gaus", "0");
        TF1 *tmpf = h_resT_zoom[i]->GetFunction("gaus");
        tmpf->Draw("lsame");
        fout->WriteTObject(c.back(), c.back()->GetName());
        c.back()->SaveAs(TString(c.back()->GetName()).ReplaceAll(".", "-") + ".pdf");
        myfile << Form("zf %d %.6f %.6f\n", i, tmpf->GetParameter(1), tmpf->GetParameter(2));
    }

    printf("Tot entries: %d\n", nentries);
    printf("Entries passing selection: %d\n", nentries_selected);
    myfile << "totEntries " << nentries << endl;
    myfile << "selEntries " << nentries_selected << endl;
    for (Int_t i = 0; i < nch; ++i){
        vector<Int_t> colors = {kRed, kGreen+2, kBlue, kMagenta, kCyan, kGreen, kOrange};
        Int_t icolor = 0;

        

        for (Int_t j=0; j<(Int_t)Nsigmas.size(); ++j){
            Double_t t = (Double_t)nentries_selected;
            Double_t p = (Double_t)(nentries_Nsigma[i][j]);
            Double_t eff = p/t;
            printf("ch: %d; Nsigma: %.1f; passed: %.0f; eff: %.6f \n", i, Nsigmas[j], p, eff);
            myfile << Form("%d %.1f %.0f %.6f\n", i, Nsigmas[j], p, eff);
        }     

        TString ncanv = Form("c_%s", h_resT[i]->GetName());
        c.push_back(new TCanvas(ncanv, ncanv));
        c.back()->cd();
        h_resT[i]->SetLineWidth(2);
        h_resT[i]->SetLineColor(kBlack);
        h_resT[i]->Draw();
        for (auto n : Nsigmas){
            Double_t x1 = mean_resT_check[i] - n * sigma_resT_check[i];
            Double_t x2 = mean_resT_check[i] + n * sigma_resT_check[i];
            Double_t y1 = h_resT[i]->GetMinimum();
            Double_t y2 = h_resT[i]->GetMaximum();
            TLine *l1 = new TLine(x1, y1, x1, y2);
            l1->SetLineColor(colors[icolor]);
            l1->SetLineStyle(kSolid);
            l1->SetLineWidth(1);
            l1->Draw("lsame");
            TLine *l2 = new TLine(x2, y1, x2, y2);
            l2->SetLineColor(colors[icolor]);
            l2->SetLineStyle(kSolid);
            l2->SetLineWidth(1);
            l2->Draw("lsame");
            icolor =  ((icolor>=(Int_t)colors.size()-1)? 0 : icolor+1);
        }
    }

    { // Exporting h_xywc 
        TString ncanv = Form("c_%s", h_xywc->GetName());
        c.push_back(new TCanvas(ncanv, ncanv));
        c.back()->cd();
        h_xywc->Draw("colz");
        c.back()->SaveAs(TString(c.back()->GetName()).ReplaceAll(".", "-") + ".pdf");
        fout->WriteTObject(c.back(), c.back()->GetName());
    }
    
    for (auto& hh : {h_resT, h_max})
        for (auto h : hh)
            fout->WriteTObject(h, h->GetName());
    for (auto& hh: hh_max)
        for (auto h : hh)
            fout->WriteTObject(h, h->GetName());

    fout->Close();
    myfile.close();
    //fin->Close();
    // TCanvas *c1 = new TCanvas();
    // h_resT->Draw("hist");
    // h_resT->Fit("gaus");
    return 1;
}