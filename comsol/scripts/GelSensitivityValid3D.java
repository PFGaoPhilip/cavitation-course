import com.comsol.model.*;
import com.comsol.model.util.*;
import java.util.Arrays;
public class GelSensitivityValid3D {
 static final String ROOT="./";
 static void interp(Model m,String tag,String unit,String[][] rows) {
  m.func().create(tag,"Interpolation");m.func(tag).set("funcname",tag);m.func(tag).set("source","table");m.func(tag).set("nargs",1);m.func(tag).set("table",rows);m.func(tag).set("argunit",new String[]{"1"});m.func(tag).set("fununit",unit);m.func(tag).set("interp","linear");
 }
 public static Model run()throws Exception {
  Model m=ModelUtil.load("pfc_gel_material_sensitivity_3d",ROOT+"scratch/free_coreshell3d_fine_solved.mph");
  m.label("Theory 2: finite-energy PFP / 3D PAAm conditional feasibility and interface sensitivity");
  m.param().set("caseIndex","0","0: bare reference; 1/2: inner-tension bracket; 3: stronger gel; 4/5: coated-interface alternatives");
  interp(m,"Gcase","Pa",new String[][]{{"0","10000"},{"1","10000"},{"2","10000"},{"3","27027.027027"},{"4","27027.027027"},{"5","10000"}});
  interp(m,"LLcase","N/m",new String[][]{{"0","0.053999999999999999"},{"1","0.053999999999999999"},{"2","0.053999999999999999"},{"3","0.053999999999999999"},{"4","0.00114"},{"5","0.00114"}});
  interp(m,"LVcase","N/m",new String[][]{{"0","0.00941"},{"1","0.0080000000000000002"},{"2","0.014"},{"3","0.00941"},{"4","0.00941"},{"5","0.00941"}});
  interp(m,"rhoColdCase","kg/m^3",new String[][]{{"0","1623.3028161533516"},{"1","1623.3028161533516"},{"2","1623.3028161533516"},{"3","1623.3028161533516"},{"4","1621.4258409997951"},{"5","1621.4258409997951"}});
  m.param().set("G","Gcase(caseIndex)");m.param().set("sigLL","LLcase(caseIndex)");m.param().set("sigLV","LVcase(caseIndex)");m.param().set("rhoD","rhoColdCase(caseIndex)");
  m.param().set("lam","2.5441334743639912","Initial-guess stretch only; no imposed radius or shape");
  m.component("c").physics("ge").feature("ge1").set("initialValueU",new String[]{"1.1398107875349053","-0.093845518489624163","1.3349352599864706"});

  m.study().create("sensitivity");m.study("sensitivity").label("Four admissible continuum material/interface alternatives at fixed 13 pJ retained energy");m.study("sensitivity").create("stat","Stationary");m.study("sensitivity").feature("stat").set("geometricNonlinearity",true);
  m.study("sensitivity").feature("stat").set("useparam","on");m.study("sensitivity").feature("stat").set("pname",new String[]{"caseIndex","Qdep"});m.study("sensitivity").feature("stat").set("plistarr",new String[]{"0 1 2 3","13 13 13 13"});m.study("sensitivity").feature("stat").set("punit",new String[]{"","pJ"});m.study("sensitivity").feature("stat").set("preusesol","yes");m.study("sensitivity").createAutoSequences("all");
  String sol=m.study("sensitivity").getSolverSequences("all")[0];System.out.println("SENSITIVITY_SOLVER="+sol);m.sol(sol).feature("v1").set("initmethod","init");
  m.sol(sol).feature("v1").feature("c_u").set("scalemethod","manual");m.sol(sol).feature("v1").feature("c_u").set("scaleval","a");m.sol(sol).feature("v1").feature("c_solid_hyp_pw").set("scalemethod","manual");m.sol(sol).feature("v1").feature("c_solid_hyp_pw").set("scaleval","G");m.sol(sol).feature("v1").feature("c_ODE1").set("scalemethod","manual");m.sol(sol).feature("v1").feature("c_ODE1").set("scaleval","1");
  m.sol(sol).feature("s1").create("directAll","Direct");m.sol(sol).feature("s1").feature("directAll").set("linsolver","pardiso");m.sol(sol).feature("s1").create("fullAll","FullyCoupled");m.sol(sol).feature("s1").feature("fullAll").set("linsolver","directAll");m.sol(sol).feature("s1").feature("fullAll").set("maxiter",12);
  if(Arrays.asList(m.sol(sol).feature("s1").feature().tags()).contains("se1"))m.sol(sol).feature("s1").feature().remove("se1");m.sol(sol).feature("s1").set("stol","1e-7");
  m.save(ROOT+"scratch/gel_sensitivity3d_valid_configured.mph");try{m.sol(sol).runAll();}catch(Exception e){m.save(ROOT+"scratch/gel_sensitivity3d_valid_failed.mph");throw e;}
  String ds="sensitivityData";m.result().dataset().create(ds,"Solution");m.result().dataset(ds).set("solution",sol);
  m.result().table().create("sensTable","Table");m.result().numerical().create("sensEval","EvalGlobal");m.result().numerical("sensEval").set("data",ds);m.result().numerical("sensEval").set("table","sensTable");
  String[] ex={"caseIndex","Qdep","G","sigLL","sigLV","c.stretch","c.Temp","c.fv","c.Rg","c.shellThickness","c.Qmin","(c.Qmin-Qdep)/Qdep","c.massResidual","c.pLP","c.pVP","c.pVP-c.pLP-2*sigLV/c.Rg","c.gLP-c.gVP","c.pGel","G/2*(5-4/c.stretch-c.stretch^(-4))","c.WsTotal","c.Afree/(4*pi*c.Rfree^2)","c.maxd(c.stretchMax)","c.maxd(c.stretchMax)/lamFail","c.Rg/nucleusFloor"};
  m.result().numerical("sensEval").set("expr",ex);m.result().numerical("sensEval").set("descr",ex);m.result().numerical("sensEval").setResult();m.result().table("sensTable").save(ROOT+"data/gel_sensitivity3d_valid_control.csv");m.save(ROOT+"scratch/gel_sensitivity3d_valid_solved.mph");System.out.println("SENSITIVITY_3D_SOLVED="+Arrays.toString(m.sol(sol).getSize()));return m;
 }
 public static void main(String[]args)throws Exception{run();}
}
