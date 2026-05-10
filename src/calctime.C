void calctime(TString filename, TString dirName = ".") {
  TTree t1;
  TH1D *h1 = new TH1D("h1","h1",100,-0.4,0.4);
  t1.ReadFile(dirName+"/output_train_"+filename,"t:xwc0:ywc0");
  t1.Draw("t>>h1","","goff");
  h1->Fit("gaus","0");
  double sigma_train = h1->GetFunction("gaus")->GetParameter(2);

  TTree t2;
  TH1D *h2 = new TH1D("h2","h2",100,-0.4,0.4);
  t2.ReadFile(dirName+"/output_eval_"+filename,"t:xwc0:ywc0");
  t2.Draw("t>>h2","","goff");
  h2->Fit("gaus","0");
  double sigma_eval = h2->GetFunction("gaus")->GetParameter(2);

  TTree t3;
  TH1D *h3 = new TH1D("h3","h3",100,-0.4,0.4);
  t3.ReadFile(dirName+"/output_target_"+filename,"t:xwc0:ywc0");
  t3.Draw("t>>h3","","goff");
  h3->Fit("gaus","0");
  double sigma_mcp = h3->GetFunction("gaus")->GetParameter(2);

  double res_test = 1000*sqrt(sigma_eval*sigma_eval - 0.25*sigma_mcp*sigma_mcp);
  double res_train = 1000 * sqrt(sigma_train * sigma_train + 0.25 * sigma_mcp * sigma_mcp);
  cout << "Resolution Test= " << res_test << " ps" << endl;
  
  ofstream myfile;
  myfile.open("resolution.txt");

  myfile << "Sigma mcp  = " << sigma_mcp*1000 << " ps" << endl;
  myfile << "Sigma train= " << sigma_train*1000 << " ps" << endl;
  myfile << "Sigma test = " << sigma_eval*1000 << " ps" << endl;
  myfile << "Resolution train= " << res_train << " ps" << endl;
  myfile << "Resolution test = " << res_test << " ps" << endl;

  myfile.close();
  
}
