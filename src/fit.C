void fit(string filename) {
  TCanvas *c1 = new TCanvas();
  TTree t1;
  TH1D *h1 = new TH1D("h1","h1",100,-0.4,0.4);
  t1.ReadFile((string("output_train_")+filename).c_str(),"t:xwc2:ywc2");
  t1.Draw("t>>h1");
  h1->Fit("gaus");

  TCanvas *c2 = new TCanvas();
  TTree t2;
  TH1D *h2 = new TH1D("h2","h2",100,-0.4,0.4);
  t2.ReadFile((string("output_eval_")+filename).c_str(),"t:xwc2:ywc2");
  t2.Draw("t>>h2");
  h2->Fit("gaus");
  double sigma_eval = h2->GetFunction("gaus")->GetParameter(2);

  TCanvas *c3 = new TCanvas();
  TTree t3;
  TH1D *h3 = new TH1D("h3","h3",100,-0.4,0.4);
  t3.ReadFile((string("output_target_")+filename).c_str(),"t:xwc2:ywc2");
  t3.Draw("t>>h3");
  h3->Fit("gaus");
  double sigma_mcp = h3->GetFunction("gaus")->GetParameter(2);

  cout << "Resolution = " << 1000*sqrt(sigma_eval*sigma_eval - 0.25*sigma_mcp*sigma_mcp) << " ps" << endl;

  TCanvas *c4 = new TCanvas();
  TTree t4;
  TH2D *h4 = new TH2D("h4","h4",100,-25, 30, 100, -35, 20);
  t4.ReadFile((string("output_data_")+filename).c_str(),"run:xwc2:ywc2:max0:max1:max2:max3");
  t4.Draw("ywc2:xwc2>>h4","","zcol");

  TCanvas *c5 = new TCanvas();
  TProfile2D *h5 = new TProfile2D("h5","h5",100,-25, 30, 100, -35, 20, 0, 1);
  t4.Draw("max0+max1+max2+max3:ywc2:xwc2>>h5","","prof zcol");

  TCanvas *c6 = new TCanvas();
  TProfile2D *h6 = new TProfile2D("h6","h6",100,-25, 30, 100, -35, 20, -0.05, 0.05,"s");
  t1.Draw("t:ywc2:xwc2>>h6","","goff");
  h6->Draw("zcol");

  TCanvas *c7 = new TCanvas();
  TH2D *h7 = new TH2D("h7","h7",100,-25, 30, 100, -35, 20);
  for(int i=1; i<101; ++i) {
    for(int j=1; j<101; ++j) {
       h7->SetBinContent(i, j, h6->GetBinError(i, j));
    }
  }
  h7->Draw("zcol");
}
