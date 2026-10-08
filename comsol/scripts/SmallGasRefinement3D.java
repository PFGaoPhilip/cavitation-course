import com.comsol.model.*;
import com.comsol.model.util.*;
import java.util.Arrays;
/** Resolve the short pulse in gas case 0 without repeating the other scenarios. */
public class SmallGasRefinement3D {
 static final String ROOT="./";
 public static Model run()throws Exception{
  Model m=ModelUtil.load("small_gas_accuracy_correction",ROOT+"scratch/pressure_envelope3d_solved.mph");m.param().set("gasCase","0");
  m.study("stdcG").label("Seven baseline gas cases at 25 ns: short-pulse case 0 requires the separate refinement study");
  m.study().create("smallGasRefinement");m.study("smallGasRefinement").label("Authoritative small gas case 0: 6.25 ns internal, 12.5 ns output; other physics disabled");m.study("smallGasRefinement").create("time","Transient");m.study("smallGasRefinement").feature("time").set("tlist","range(0,12.5[ns],8[us])");
  for(String cc:m.component().tags())for(String ph:m.component(cc).physics().tags())m.study("smallGasRefinement").feature("time").setSolveFor(m.component(cc).physics(ph).resolveModelPath(),cc.equals("cG"));
  m.study("smallGasRefinement").feature("time").set("useparam","on");m.study("smallGasRefinement").feature("time").set("pname",new String[]{"gasCase"});m.study("smallGasRefinement").feature("time").set("plistarr",new String[]{"0"});m.study("smallGasRefinement").feature("time").set("punit",new String[]{""});m.study("smallGasRefinement").createAutoSequences("all");String sol=m.study("smallGasRefinement").getSolverSequences("all")[0];
  m.sol(sol).feature("v1").set("initmethod","init");for(String tag:m.sol(sol).feature("v1").feature().tags()){m.sol(sol).feature("v1").feature(tag).set("scalemethod","manual");m.sol(sol).feature("v1").feature(tag).set("scaleval","1");}
  m.sol(sol).feature("t1").create("direct","Direct");m.sol(sol).feature("t1").feature("direct").set("linsolver","pardiso");m.sol(sol).feature("t1").create("coupled","FullyCoupled");m.sol(sol).feature("t1").feature("coupled").set("linsolver","direct");m.sol(sol).feature("t1").feature("coupled").set("maxiter",20);
  for(String tag:new String[]{"se1","fc1"})if(Arrays.asList(m.sol(sol).feature("t1").feature().tags()).contains(tag))m.sol(sol).feature("t1").feature().remove(tag);
  m.sol(sol).feature("t1").set("rtol","2e-5");m.sol(sol).feature("t1").set("timemethod","genalpha");m.sol(sol).feature("t1").set("rhoinf",.75);m.sol(sol).feature("t1").set("tstepsgenalpha","manual");m.sol(sol).feature("t1").set("timestepgenalpha","6.25[ns]");
  try{m.sol(sol).runAll();}catch(Exception e){m.save(ROOT+"scratch/small_gas_refinement_failed.mph");throw e;}
  m.result().dataset().create("smallGasData","Solution");m.result().dataset("smallGasData").set("solution",sol);m.result().dataset("smallGasData").set("comp","cG");m.result().table().create("smallGasTable","Table");m.result().numerical().create("smallGasEval","EvalGlobal");m.result().numerical("smallGasEval").set("data","smallGasData");m.result().numerical("smallGasEval").set("table","smallGasTable");
  String[] ex={"gasCase","t","t/taucG","acG","betacG","E0cG","DP*cG.pdet","cG.idcG(cG.pAc)/cG.idcG(1)","cG.r1","cG.U1","cG.pg1","cG.pB1","cG.En","cG.Ei","cG.Ep","cG.Ea","E0cG*cG.ediss","E0cG*cG.erout","(cG.En+cG.Ei+cG.Ep+cG.Ea+E0cG*(cG.ediss+cG.erout)-E0cG)/E0cG","abs(cG.U1)/cL"};
  m.result().numerical("smallGasEval").set("expr",ex);m.result().numerical("smallGasEval").set("descr",ex);m.result().numerical("smallGasEval").setResult();m.result().table("smallGasTable").save(ROOT+"data/refined_gas_small.csv");
  m.save(ROOT+"scratch/pressure_envelope3d_validated.mph");System.out.println("SMALL_GAS_CORRECTION_SOLVED="+Arrays.toString(m.sol(sol).getSize()));return m;
 }
 public static void main(String[]args)throws Exception{run();}
}
