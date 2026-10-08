import com.comsol.model.*;
import com.comsol.model.util.*;
import java.util.Arrays;
/** Native final save and authentic COMSOL exports from the clean solved model. */
public class FinalModelB3D {
 static final String ROOT="./";
 static void exportImage(Model m,String tag,String pg,String filename){
  m.result().export().create(tag,pg,"Image");m.result().export(tag).set("pngfilename",ROOT+"plots/"+filename);
  m.result().export(tag).set("zoomextents",false);m.result().export(tag).set("colortheme","Light");m.result().export(tag).set("options3d",true);m.result().export(tag).set("logo3d",false);m.result().export(tag).run();
 }
 static void view(Model m,String tag,double[] pos,double angle){
  m.component("c").view().create(tag,3);m.component("c").view(tag).camera().set("position",pos);
  m.component("c").view(tag).camera().set("target",new double[]{0,0,0});m.component("c").view(tag).camera().set("up",new double[]{0,0,1});m.component("c").view(tag).camera().set("projection","perspective");m.component("c").view(tag).camera().set("zoomanglefull",angle);m.component("c").view(tag).camera().set("autoupdate",false);
 }
 public static Model run()throws Exception{
  Model m=ModelUtil.load("model_B_verified_3d",ROOT+"scratch/gel_sensitivity3d_valid_solved.mph");
  m.label("Model B: finite PFP inventory and 3D reference PAAm — conditional embedding feasibility");m.modelPath(ROOT+"final");m.param().set("caseIndex","0");
  m.param().set("sig","sigLL","Unused legacy alias: assumed PFP/gel outer coefficient; active loads use sigLL");
  m.param().set("caseIndex","0","Only 0–3 are the four solved material/interface sensitivity alternatives");
  m.func("Gcase").set("table",new String[][]{{"0","10000"},{"1","10000"},{"2","10000"},{"3","27027.027027"}});
  m.func("LLcase").set("table",new String[][]{{"0","0.054"},{"1","0.054"},{"2","0.054"},{"3","0.054"}});
  m.func("LVcase").set("table",new String[][]{{"0","0.00941"},{"1","0.008"},{"2","0.014"},{"3","0.00941"}});
  m.func("rhoColdCase").set("table",new String[][]{{"0","1623.3028161533516"},{"1","1623.3028161533516"},{"2","1623.3028161533516"},{"3","1623.3028161533516"}});
  m.param().set("lam","1.8","Baseline initial-guess stretch only; no imposed cavity displacement. Before sensitivity recomputation use 2.5441334743639912.");
  m.component("c").physics("ge").feature("ge1").set("initialValueU",new String[]{"1.1655711769961976","-0.11475258143625314","1.5473196370961337"});
  m.study("std").label("Five verified energy states: original baseline initialization restored by default");
  m.study("sensitivity").label("Four solved 13 pJ cases: set documented sensitivity initial guesses before recomputing");
  m.param().set("opticalCalibrationKnown","0","Absorption cross section and current gel formulation are unknown; Qdep is retained energy, not fluence");
  m.param().set("coatedCaseAccepted","0","Coated 3–4 nm films and divergent native equilibria are excluded; diagnostics retained outside final model");
  view(m,"fieldView",new double[]{1.8e-6,-2.4e-6,1.8e-6},30);
  view(m,"meshView",new double[]{-10e-6,-12e-6,9e-6},60);
  m.result().dataset().create("finalCavity","Surface");m.result().dataset("finalCavity").set("data","dset1");m.result().dataset("finalCavity").selection().named("cavity");
  m.result().create("finalGelField",3);m.result("finalGelField").label("Freely responding 3D cavity: local principal stretch, Q=11.65 pJ");m.result("finalGelField").set("data","finalCavity");m.result("finalGelField").set("view","fieldView");m.result("finalGelField").set("solrepresentation","solnum");m.result("finalGelField").set("solnum",2);
  m.result("finalGelField").create("surface","Surface");m.result("finalGelField").feature("surface").set("expr","mean(c.stretchMax)");m.result("finalGelField").feature("surface").set("unit","1");
  m.result("finalGelField").feature("surface").create("deformed","Deform");m.result("finalGelField").feature("surface").feature("deformed").set("expr",new String[]{"u","v","w"});m.result("finalGelField").feature("surface").feature("deformed").set("scale",1);
  exportImage(m,"fieldImage","finalGelField","native_B_principal_stretch.png");
  m.result().dataset().create("finalMeshData","Mesh");m.result().dataset("finalMeshData").set("mesh","mesh");
  m.result().create("finalGelMesh",3);m.result("finalGelMesh").label("Native undeformed 3D gel mesh: X >= 0 cutaway, initial cavity radius 300 nm");m.result("finalGelMesh").set("data","finalMeshData");m.result("finalGelMesh").set("view","meshView");m.result("finalGelMesh").create("mesh","Mesh");
  m.result("finalGelMesh").feature("mesh").set("meshdomain","volume");m.result("finalGelMesh").feature("mesh").set("filteractive","on");m.result("finalGelMesh").feature("mesh").set("elemfilter","logicexpression");m.result("finalGelMesh").feature("mesh").set("logfilterexpr","x>=0");m.result("finalGelMesh").feature("mesh").set("resolution","norefine");
  exportImage(m,"meshImage","finalGelMesh","native_B_mesh.png");
  m.save(ROOT+"final/Model_B_PFP_Hydrogel_Feasibility_3D.mph");
  m.result().report().create("nativeConfiguration","Report");m.result().report("nativeConfiguration").set("format","html");m.result().report("nativeConfiguration").set("level","complete");m.result().report("nativeConfiguration").set("filename",ROOT+"native-config/B/Model_B.html");m.result().report("nativeConfiguration").set("alwaysask",false);m.result().report("nativeConfiguration").set("openwhenfinished",false);m.result().report("nativeConfiguration").generate();m.result().report("nativeConfiguration").run();
  m.save(ROOT+"final/Model_B_PFP_Hydrogel_Feasibility_3D.mph");
  for(String sol:m.sol().tags())System.out.println("FINAL_B_SOLUTION="+sol+" SIZE="+Arrays.toString(m.sol(sol).getSize())+" PARAMS="+Arrays.toString(m.sol(sol).getPNames())+" VALUES="+Arrays.toString(m.sol(sol).getPVals()));
  System.out.println("FINAL_MODEL_B_SAVED_WITH_NATIVE_EXPORTS");return m;
 }
 public static void main(String[]args)throws Exception{run();}
}
