#include <iostream>
using namespace std;
#include "TFile.h"
#include "TTree.h"
#include "TString.h"
#include "TProfile.h"
#include "TProfile2D.h"
#include "TSpline.h"

TGraph invertCalib(TH1* h){
    Int_t Nbins = h->GetNbinsX();
    vector<Double_t> x, y;
    for (Int_t ibin=1; ibin<=Nbins; ++ibin){
        x.push_back(h->GetBinCenter(ibin));
        y.push_back(h->GetBinContent(ibin));
    }
    Double_t tmpmax = y[0];
    for (Int_t i=1; i<Nbins; ++i){
        if (y[i-1] > y[i]) {
            tmpmax = y[i-1];
            y[i-1] = y[i];
            y[i] = tmpmax;
            i = 1;
        } 
    }
    TGraph gp(Nbins, y.data(), x.data());
    gp.Print("v");
    gp.SetBit(TGraph::kIsSortedX);
    gp.SetName(TString("g_") + h->GetName());
    gp.SetTitle(TString("g_") + h->GetName());
    // TSpline3 spline(TString("spline")+h->GetName(), &gp);
    // spline.SetName(TString("spline") + h->GetName());
    return gp;
}
int correctPositionBias(TString nfinVal){
    
    TTree tinV("tinV", "tinV");
    tinV.ReadFile(nfinVal, "xp:yp:xt:yt:max1:max2:max3:max4");
    // Double_t xmin = -8.8 - 7;
    // Double_t xmax = +16.2 + 7;
    // Double_t ymin = -22 - 7;
    // Double_t ymax = +3 + 7;
    Double_t xmin = -8.8;
    Double_t xmax = +16.2;
    Double_t ymin = -22;
    Double_t ymax = +3;

    TProfile pfx("pfx", "pfx; xt [mm]; xp [mmm]", 75, xmin-7, xmax+7);
    TProfile pfy("pfy", "pfy; yt [mm]; yp [mmm]", 75, ymin-7, ymax+7);
    //TString posCut = Form("xt > %g && xt < %g && yt > %g && yt < %g", xmin, xmax, ymin, ymax);
    //TString posCut = Form("xp > %g && xp < %g && yp > %g && yp < %g", xmin, xmax, ymin, ymax);
    TString posCut = "1";
    cout << "posCut " << posCut.Data() << endl;
    tinV.Draw("xp:xt>>pfx", posCut, "prof goff");
    tinV.Draw("yp:yt>>pfy", posCut, "prof goff");
    auto calibx = invertCalib(&pfx);
    calibx.Print("v");
    auto caliby = invertCalib(&pfy);
    caliby.Print("v");

    float xp, yp;
    tinV.SetBranchAddress("xp", &xp);
    tinV.SetBranchAddress("yp", &yp);
    int nentries = tinV.GetEntries();
    TTree *tout = tinV.CloneTree(0);
    tout->SetName("t");
    tout->SetTitle("t");
    float xc, yc;
    tout->Branch("xc", &xc, "xc/F");
    tout->Branch("yc", &yc, "yc/F");
    int ibinx, ibiny;
    for (int ientry=0; ientry<nentries; ++ientry){
        tinV.GetEntry(ientry);
        xc = calibx.Eval(xp);
        yc = caliby.Eval(yp);
        //printf("%g %g\n", xc,yc);
        tout->Fill();
    }

    TFile* fout =  new TFile("correctPositionBias.root", "RECREATE");
    fout->WriteTObject(&pfx, pfx.GetName());
    fout->WriteTObject(&pfy, pfy.GetName());
    fout->WriteTObject(&calibx, calibx.GetName());
    fout->WriteTObject(&caliby, caliby.GetName());
    fout->WriteTObject(tout, tout->GetName());
    //fout.Close();
    return 1;
}