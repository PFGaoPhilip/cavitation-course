import com.comsol.model.*;
import com.comsol.model.util.*;
import java.util.Arrays;
/** Native final pressure model and COMSOL-generated field/mesh/configuration. */
public class FinalModelA3D {
 static final String ROOT="./";
 static void exportImage(Model m,String tag,String pg,String filename){
  m.result().export().create(tag,pg,"Image");m.result().export(tag).set("pngfilename",ROOT+"plots/"+filename);m.result().export(tag).set("zoomextents",false);m.result().export(tag).set("colortheme","Light");m.result().export(tag).set("options3d",true);m.result().export(tag).set("logo3d",false);m.result().export(tag).run();
 }
 static void view(Model m,String tag,double[] pos,double angle){
  view(m,"cP",tag,pos,angle);
 }
 static void view(Model m,String cp,String tag,double[] pos,double angle){
  m.component(cp).view().create(tag,3);m.component(cp).view(tag).camera().set("position",pos);m.component(cp).view(tag).camera().set("target",new double[]{0,0,0});m.component(cp).view(tag).camera().set("up",new double[]{0,0,1});m.component(cp).view(tag).camera().set("projection","perspective");m.component(cp).view(tag).camera().set("zoomanglefull",angle);m.component(cp).view(tag).camera().set("autoupdate",false);
 }
 static void field(Model m,String cp,String data,String tag,int solnum,String filename,String label){
  view(m,cp,tag+"View",new double[]{-1.2e-3,-1.8e-3,1.2e-3},60);
  m.result().dataset().create(tag+"Plane","CutPlane");m.result().dataset(tag+"Plane").set("data",data);m.result().dataset(tag+"Plane").set("quickplane",cp.equals("c5")?"xy":"xz");m.result().dataset(tag+"Plane").set(cp.equals("c5")?"quickz":"quicky",0);
  m.result().create(tag,3);m.result(tag).label(label);m.result(tag).set("data",tag+"Plane");m.result(tag).set("view",tag+"View");m.result(tag).set("solrepresentation","solnum");m.result(tag).set("solnum",solnum);m.result(tag).create("surface","Surface");m.result(tag).feature("surface").set("expr",cp+".pAc");m.result(tag).feature("surface").set("unit","kPa");
  exportImage(m,tag+"Image",tag,filename);
 }
 public static Model run()throws Exception{
  Model m=ModelUtil.load("model_A_verified_3d",ROOT+"scratch/pressure_envelope3d_finalchecks.mph");m.label("Model A: conditional pressure envelope — finite PFP sources and 3D weak waves");m.modelPath(ROOT+"final");m.param().set("gasCase","0");
  for(String cp:new String[]{"cP","cG","c3","c5","cU"})m.result().dataset("data"+cp).set("comp",cp);
  m.result().dataset("smallGasData").set("comp","cG");m.result().dataset("uniformRefinedData").set("comp","cU");
  m.component("cU").label("100 PFP common-state diagnostic: local pressure variation prevents an unqualified uniform-population prediction");
  m.param().set("lambdaLaser_ref","808[nm]","Draft stamp wavelength; not an absorption calibration of these source states");m.param().set("pulse_ref","20[ms]","Draft Si reference pulse; not the modeled collapse duration");m.param().set("Qheat_draft","11.376[W]*pulse_ref","Integrated draft heating-source budget, unreconciled with incident power; not local PFP absorption");m.param().set("etaBookkeeping","E0cP/Qheat_draft","Only a bookkeeping ratio for the declared 55 nJ state; not a measured conversion efficiency");m.param().set("jetResolved","0","No jet, shock, stagnation or wall impact is resolved by this pressure formulation");
  view(m,"pressureFieldView",new double[]{-1.2e-3,-1.8e-3,1.2e-3},48);
  view(m,"pressureMeshView",new double[]{-1.3e-3,-1.4e-3,1.0e-3},60);
  m.result().dataset().create("finalPressurePlane","CutPlane");m.result().dataset("finalPressurePlane").set("data","datacP");m.result().dataset("finalPressurePlane").set("quickplane","xz");m.result().dataset("finalPressurePlane").set("quicky",0);
  m.result().create("finalPressureField",3);m.result("finalPressureField").label("Native 3D water pressure: single finite-PFP source at receiver peak, t=5.025 us");m.result("finalPressureField").set("data","finalPressurePlane");m.result("finalPressureField").set("view","pressureFieldView");m.result("finalPressureField").set("solrepresentation","solnum");m.result("finalPressureField").set("solnum",202);m.result("finalPressureField").create("surface","Surface");m.result("finalPressureField").feature("surface").set("expr","cP.pAc");m.result("finalPressureField").feature("surface").set("unit","kPa");
  exportImage(m,"pressureFieldImage","finalPressureField","native_A_pressure_field.png");
  field(m,"c5","datac5","fivePfpField",132,"native_A_five_PFP_field.png","Native 3D gauge pressure: five PFP sources, t=3.275 us; fixed total 55 nJ");
  field(m,"cU","uniformRefinedData","uniformPfpField",159,"native_A_uniform_PFP_field.png","Native 3D gauge pressure: diagnostic common-state PFP population, t=1.975 us");
  m.result().dataset().create("finalPressureMeshData","Mesh");m.result().dataset("finalPressureMeshData").set("mesh","meshcP");m.result().create("finalPressureMesh",3);m.result("finalPressureMesh").label("Native 3D water mesh: x>=0 cutaway; source matching region and finite receiver");m.result("finalPressureMesh").set("data","finalPressureMeshData");m.result("finalPressureMesh").set("view","pressureMeshView");m.result("finalPressureMesh").create("mesh","Mesh");m.result("finalPressureMesh").feature("mesh").set("meshdomain","volume");m.result("finalPressureMesh").feature("mesh").set("filteractive","on");m.result("finalPressureMesh").feature("mesh").set("elemfilter","logicexpression");m.result("finalPressureMesh").feature("mesh").set("logfilterexpr","x>=0");m.result("finalPressureMesh").feature("mesh").set("resolution","norefine");exportImage(m,"pressureMeshImage","finalPressureMesh","native_A_mesh.png");
  m.save(ROOT+"final/Model_A_Conditional_Pressure_Envelope_3D.mph");
  m.result().report().create("nativeConfiguration","Report");m.result().report("nativeConfiguration").set("format","html");m.result().report("nativeConfiguration").set("level","complete");m.result().report("nativeConfiguration").set("filename",ROOT+"native-config/A/Model_A.html");m.result().report("nativeConfiguration").set("alwaysask",false);m.result().report("nativeConfiguration").set("openwhenfinished",false);m.result().report("nativeConfiguration").generate();m.result().report("nativeConfiguration").run();
  m.save(ROOT+"final/Model_A_Conditional_Pressure_Envelope_3D.mph");
  for(String cp:m.component().tags())System.out.println("FINAL_A_COMPONENT="+cp+" DIMENSION="+m.component(cp).geom("g"+cp).getSDim());
  for(String sol:m.sol().tags())System.out.println("FINAL_A_SOLUTION="+sol+" SIZE="+Arrays.toString(m.sol(sol).getSizeMulti()));
  System.out.println("FINAL_MODEL_A_SAVED_WITH_NATIVE_EXPORTS");return m;
 }
 public static void main(String[]args)throws Exception{run();}
}
