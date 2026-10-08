import com.comsol.model.*;
import com.comsol.model.util.*;
import java.util.Arrays;
/** Population phase-constraint/time refinement, with all other solved studies preserved. */
public class UniformPfpFinalRefinement3D {
 static final String ROOT="./";
 public static Model run()throws Exception {
  Model m=ModelUtil.load("uniform_pfp_accuracy_correction",ROOT+"scratch/pressure_envelope3d_validated.mph");
  m.component("cU").cpl().create("maxpopcU","Maximum");m.component("cU").cpl("maxpopcU").selection().geom("gcU",3);m.component("cU").cpl("maxpopcU").selection().named("populationcU");
  m.component("cU").cpl().create("minpopcU","Minimum");m.component("cU").cpl("minpopcU").selection().geom("gcU",3);m.component("cU").cpl("minpopcU").selection().named("populationcU");
  m.study("stdcU").label("Population baseline at 25 ns: phase constraints require the separate refinement study");
  m.study().create("uniformPfpRefinement");m.study("uniformPfpRefinement").label("Authoritative uniform PFP: 6.25 ns internal, 12.5 ns output, other physics disabled");
  m.study("uniformPfpRefinement").create("time","Transient");m.study("uniformPfpRefinement").feature("time").set("tlist","range(0,12.5[ns],8[us])");
  for(String cc:m.component().tags())for(String ph:m.component(cc).physics().tags())m.study("uniformPfpRefinement").feature("time").setSolveFor(m.component(cc).physics(ph).resolveModelPath(),cc.equals("cU"));
  m.study("uniformPfpRefinement").createAutoSequences("all");String sol=m.study("uniformPfpRefinement").getSolverSequences("all")[0];
  m.sol(sol).feature("v1").set("initmethod","init");
  for(String tag:m.sol(sol).feature("v1").feature().tags()){m.sol(sol).feature("v1").feature(tag).set("scalemethod","manual");m.sol(sol).feature("v1").feature(tag).set("scaleval","1");}
  m.sol(sol).feature("t1").create("direct","Direct");m.sol(sol).feature("t1").feature("direct").set("linsolver","pardiso");
  m.sol(sol).feature("t1").create("coupled","FullyCoupled");m.sol(sol).feature("t1").feature("coupled").set("linsolver","direct");m.sol(sol).feature("t1").feature("coupled").set("maxiter",20);
  for(String tag:new String[]{"se1","fc1"})if(Arrays.asList(m.sol(sol).feature("t1").feature().tags()).contains(tag))m.sol(sol).feature("t1").feature().remove(tag);
  m.sol(sol).feature("t1").set("rtol","2e-6");m.sol(sol).feature("t1").set("timemethod","genalpha");m.sol(sol).feature("t1").set("rhoinf",.75);m.sol(sol).feature("t1").set("tstepsgenalpha","manual");m.sol(sol).feature("t1").set("timestepgenalpha","6.25[ns]");
  try{m.sol(sol).runAll();}catch(Exception e){m.save(ROOT+"scratch/uniform_pfp_refinement_failed.mph");throw e;}
  m.result().dataset().create("uniformRefinedData","Solution");m.result().dataset("uniformRefinedData").set("solution",sol);m.result().dataset("uniformRefinedData").set("comp","cU");
  m.result().table().create("uniformRefinedTable","Table");m.result().numerical().create("uniformRefinedEval","EvalGlobal");m.result().numerical("uniformRefinedEval").set("data","uniformRefinedData");m.result().numerical("uniformRefinedEval").set("table","uniformRefinedTable");
  String[] ex=new String[]{"t","t/taucU","E0cU","cU.pdet*DP","cU.idcU(cU.pAc)/cU.idcU(1)","cU.r1","cU.U1","cU.pLP1","cU.pVP1","cU.Temp1","cU.fv1","cU.Rg1","cU.R1-cU.Rg1","abs(cU.U1)/cL","(cU.Sspec1-S0cU)/(100[J/(kg*K)])","cU.pVP1-cU.pLP1-2*sigIcU/cU.Rg1","cU.gLP1-cU.gVP1","cU.En","cU.Ei","cU.Ep","cU.Ea","E0cU*cU.ediss","E0cU*cU.erout","(cU.En+cU.Ei+cU.Ep+cU.Ea+E0cU*(cU.ediss+cU.erout)-E0cU)/E0cU","100*cU.Vb1/cU.ipcU(1)","cU.ipcU(cU.pAc)/cU.ipcU(1)","cU.maxpopcU(cU.pAc)","cU.minpopcU(cU.pAc)"};
  m.result().numerical("uniformRefinedEval").set("expr",ex);m.result().numerical("uniformRefinedEval").set("descr",ex);m.result().numerical("uniformRefinedEval").setResult();m.result().table("uniformRefinedTable").save(ROOT+"data/refined_phase_uniform.csv");
  m.save(ROOT+"scratch/pressure_envelope3d_finalchecks.mph");System.out.println("UNIFORM_PFP_CORRECTION_SOLVED="+Arrays.toString(m.sol(sol).getSize()));return m;
 }
 public static void main(String[]args)throws Exception{run();}
}
