package generic;

import generalType2zSlices.system.GenT2z_Rulebase;
import generalType2zSlices.system.multicore.FLCPoolFactory;
import intervalType2.system.IT2_Rulebase;
import type1.system.T1_Rulebase;
import generalType2zSlices.sets.*;
import generalType2zSlices.system.*;
import type1.sets.*;
import type1.system.*;
import intervalType2.sets.*;
import intervalType2.system.*;
import java.text.DecimalFormat;
import java.util.concurrent.TimeUnit;
import tools.JMathPlotter;
public class test {

    long count;
    int serviceIn;
    int foodIn;
    int numberOfzLevels;
    int typeReduction;
    int xDiscs;
    int yDiscs;
    Input food,service;
    Output tip;
    T1_Rulebase rulebaseT1;
    IT2_Rulebase rulebaseIT2;
    GenT2z_Rulebase rulebaseGT2;
    FLCPoolFactory FLC;
    DecimalFormat df;
    T1MF_Triangular badFoodUMF;
    IntervalT2MF_Triangular badFoodIT2MF;
    GenT2zMF_Triangular badFoodMF;
    T1MF_Triangular greatFoodUMF;
    GenT2zMF_Triangular greatFoodMF;
    IntervalT2MF_Triangular greatFoodIT2MF;


    public test() {
        count = 200;
        serviceIn = 5;
        foodIn = 5;
        numberOfzLevels = 4;
        typeReduction = 0;
        xDiscs = 20;
        yDiscs = 20;
        df = new DecimalFormat("###.#####");
    }

    public void setup(){
        food = new Input("Food Quality",new Tuple(0,10));
        service = new Input("Service Level",new Tuple(0,10));
        tip = new Output(("Tip"),new Tuple(0,30));
        
        badFoodUMF = new T1MF_Triangular("Upper MF for bad food",0.0,0.0,10.0);
        T1MF_Triangular badFoodLMF = new T1MF_Triangular("Lower MF for bad food",0.0,0.0,8.0);
        badFoodIT2MF = new IntervalT2MF_Triangular("IT2MF for bad food",badFoodUMF,badFoodLMF);
        badFoodMF = new GenT2zMF_Triangular("zGT2MF for bad food",  badFoodIT2MF, numberOfzLevels);
        
        greatFoodUMF = new T1MF_Triangular("Upper MF for great food",0.0,10.0,10.0);
        T1MF_Triangular greatFoodLMF = new T1MF_Triangular("Lower MF for great food",2.0,10.0,10.0);
        greatFoodIT2MF = new IntervalT2MF_Triangular("IT2MF for great food",greatFoodUMF,greatFoodLMF);
        greatFoodMF =  new GenT2zMF_Triangular("zGT2MF for great food", greatFoodIT2MF,  numberOfzLevels);

        T1MF_Triangular unfriendlyServiceUMF = new T1MF_Triangular("Upper MF for unfriendly service",0.0, 0.0, 8.0);
        T1MF_Triangular unfriendlyServiceLMF = new T1MF_Triangular("Lower MF for unfriendly service",0.0, 0.0, 6.0);
        IntervalT2MF_Triangular unfriendlyServiceIT2MF = new IntervalT2MF_Triangular("IT2MF for unfriendly service",unfriendlyServiceUMF,unfriendlyServiceLMF);
        //now spawn a basic zSlices-based set with 4 zLevels
        GenT2zMF_Triangular unfriendlyServiceMF = new GenT2zMF_Triangular("zGT2MF for unfriendly service", unfriendlyServiceIT2MF, numberOfzLevels);        

        T1MF_Triangular friendlyServiceUMF = new T1MF_Triangular("Upper MF for friendly service",2.0, 10.0, 10.0);
        T1MF_Triangular friendlyServiceLMF = new T1MF_Triangular("Lower MF for friendly service",4.0, 10.0, 10.0);
        IntervalT2MF_Triangular friendlyServiceIT2MF = new IntervalT2MF_Triangular("IT2MF for friendly service",friendlyServiceUMF,friendlyServiceLMF);
        GenT2zMF_Triangular friendlyServiceMF = new GenT2zMF_Triangular("zGT2MF for friendly service", friendlyServiceIT2MF, numberOfzLevels); 

        T1MF_Gaussian lowTipUMF = new T1MF_Gaussian("Upper MF Low tip", 0.0, 6.0);
        T1MF_Gaussian lowTipLMF = new T1MF_Gaussian("Lower MF Low tip", 0.0, 4.0);
        IntervalT2MF_Gaussian lowTipIT2MF = new IntervalT2MF_Gaussian("IT2MF for Low tip",lowTipUMF,lowTipLMF);
        GenT2zMF_Gaussian lowTipMF = new GenT2zMF_Gaussian("zGT2MF for Low tip", lowTipIT2MF, numberOfzLevels);

        T1MF_Gaussian mediumTipUMF = new T1MF_Gaussian("Upper MF Medium tip", 15.0, 6.0);
        T1MF_Gaussian mediumTipLMF = new T1MF_Gaussian("Lower MF Medium tip", 15.0, 4.0);
        IntervalT2MF_Gaussian mediumTipIT2MF = new IntervalT2MF_Gaussian("IT2MF for Medium tip",mediumTipUMF,mediumTipLMF);
        GenT2zMF_Gaussian mediumTipMF = new GenT2zMF_Gaussian("zGT2MF for Medium tip", mediumTipIT2MF, numberOfzLevels);

        T1MF_Gaussian highTipUMF = new T1MF_Gaussian("Upper MF High tip", 30.0, 6.0);
        T1MF_Gaussian highTipLMF = new T1MF_Gaussian("Lower MF High tip", 30.0, 4.0);
        IntervalT2MF_Gaussian highTipIT2MF = new IntervalT2MF_Gaussian("IT2MF for High tip",highTipUMF,highTipLMF);
        GenT2zMF_Gaussian highTipMF = new GenT2zMF_Gaussian("zGT2MF for High tip", highTipIT2MF, numberOfzLevels);

        T1_Antecedent badFoodT1 = new T1_Antecedent("BadFood",badFoodUMF, food);
        T1_Antecedent greatFoodT1 = new T1_Antecedent("GreatFood",greatFoodUMF, food);

        T1_Antecedent unfriendlyServiceT1 = new T1_Antecedent("UnfriendlyService",unfriendlyServiceUMF, service);
        T1_Antecedent friendlyServiceT1 = new T1_Antecedent("FriendlyService",friendlyServiceUMF, service);

        T1_Consequent lowTipT1 =  new T1_Consequent( "LowTip", lowTipUMF, tip );
        T1_Consequent mediumTipT1 = new T1_Consequent( "MediumTip",mediumTipUMF, tip );
        T1_Consequent highTipT1 = new T1_Consequent("HighTip",highTipUMF, tip );

        rulebaseT1 = new T1_Rulebase();
        rulebaseT1.addRule(new T1_Rule(new T1_Antecedent[]{badFoodT1, unfriendlyServiceT1}, lowTipT1));
        //rulebase.addRule(new T1_Rule(new T1_Antecedent[]{badFood, okService}, lowTip));
        rulebaseT1.addRule(new T1_Rule(new T1_Antecedent[]{badFoodT1, friendlyServiceT1}, mediumTipT1));
        rulebaseT1.addRule(new T1_Rule(new T1_Antecedent[]{greatFoodT1, unfriendlyServiceT1}, lowTipT1));
        //rulebase.addRule(new T1_Rule(new T1_Antecedent[]{greatFood, okService}, mediumTip));
        rulebaseT1.addRule(new T1_Rule(new T1_Antecedent[]{greatFoodT1, friendlyServiceT1}, highTipT1));

        IT2_Antecedent badFoodIT2 = new IT2_Antecedent( "BadFood",badFoodIT2MF, food);
        IT2_Antecedent greatFoodIT2 = new IT2_Antecedent( "GreatFood",greatFoodIT2MF, food);

        IT2_Antecedent unfriendlyServiceIT2 = new IT2_Antecedent("UnfriendlyService",unfriendlyServiceIT2MF, service);
        IT2_Antecedent friendlyServiceIT2 = new IT2_Antecedent("FriendlyService",friendlyServiceIT2MF, service);

        IT2_Consequent lowTipIT2 = new IT2_Consequent( "LowTip" ,lowTipIT2MF, tip);
        IT2_Consequent mediumTipIT2 = new IT2_Consequent("MediumTip" ,mediumTipIT2MF, tip);
        IT2_Consequent highTipIT2 = new IT2_Consequent("HighTip" ,highTipIT2MF, tip);

        //set up the rulebase and add rules
        rulebaseIT2 = new IT2_Rulebase(6); 
        rulebaseIT2.addRule(new IT2_Rule(new IT2_Antecedent[]{badFoodIT2, unfriendlyServiceIT2}, lowTipIT2));
        //rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{badFood, okService}, lowTip));
        rulebaseIT2.addRule(new IT2_Rule(new IT2_Antecedent[]{badFoodIT2, friendlyServiceIT2}, mediumTipIT2));
        rulebaseIT2.addRule(new IT2_Rule(new IT2_Antecedent[]{greatFoodIT2, unfriendlyServiceIT2}, lowTipIT2));
        //rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{greatFood, okService}, mediumTip));
        rulebaseIT2.addRule(new IT2_Rule(new IT2_Antecedent[]{greatFoodIT2, friendlyServiceIT2}, highTipIT2));

         //Set up the antecedents and consequents - note how the inputs are associated...
        GenT2z_Antecedent badFood = new GenT2z_Antecedent("BadFood", badFoodMF, food);
        GenT2z_Antecedent greatFood = new GenT2z_Antecedent("GreatFood", greatFoodMF, food);

        GenT2z_Antecedent unfriendlyService = new GenT2z_Antecedent("UnfriendlyService", unfriendlyServiceMF, service);
        GenT2z_Antecedent friendlyService = new GenT2z_Antecedent("FriendlyService", friendlyServiceMF, service);

        //set up a defuzzification engine here to pass to consequents and set the discretizaiton level to 100.
        GenT2zEngine_Defuzzification gT2zED = new GenT2zEngine_Defuzzification(100);
        GenT2z_Consequent lowTip = new GenT2z_Consequent("LowTip", lowTipMF, tip, gT2zED);
        GenT2z_Consequent mediumTip = new GenT2z_Consequent("MediumTip", mediumTipMF, tip, gT2zED);
        GenT2z_Consequent highTip = new GenT2z_Consequent("HighTip", highTipMF, tip, gT2zED);

        //Set up the rulebase and add rules
        rulebaseGT2 = new GenT2z_Rulebase(6); 
        rulebaseGT2.addRule(new GenT2z_Rule(new GenT2z_Antecedent[]{badFood, unfriendlyService}, lowTip));
        //rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{badFood, okService}, lowTip));
        rulebaseGT2.addRule(new GenT2z_Rule(new GenT2z_Antecedent[]{badFood, friendlyService}, mediumTip));
        rulebaseGT2.addRule(new GenT2z_Rule(new GenT2z_Antecedent[]{greatFood, unfriendlyService}, lowTip));
        //rulebase.addRule(new IT2_Rule(new IT2_Antecedent[]{greatFood, okService}, mediumTip));
        rulebaseGT2.addRule(new GenT2z_Rule(new GenT2z_Antecedent[]{greatFood, friendlyService}, highTip));
    }

    public void getRulebaseT1Times(){
        food.setInput(foodIn);
        service.setInput(serviceIn);
        long timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseT1.evaluate(0).get(tip);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("T1 average evaluate Height time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseT1.evaluate(1).get(tip);
            timecount += System.nanoTime() - start;
        }
        System.out.println("T1 average evaluate Centroid time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
        
    }

    public void getRulebaseIT2Times(){
        food.setInput(foodIn);
        service.setInput(serviceIn);
        long timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseIT2.evaluate(0).get(tip);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("IT2 average evaluate COS time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseIT2.evaluate(1).get(tip);
            timecount += System.nanoTime() - start;
        }
        System.out.println("IT2 average evaluate Centroid time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
        food.setInput(foodIn);
        service.setInput(serviceIn);
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseIT2.evaluateGetCentroid(0).get(tip);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("IT2 average evaluate COS getCentroid time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseIT2.evaluateGetCentroid(1).get(tip);
            timecount += System.nanoTime() - start;
        }
        System.out.println("IT2 average evaluate Centroid getCentroid time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
    }

    public void getRulebaseGT2Times(){
        food.setInput(foodIn);
        service.setInput(serviceIn);
        long timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseGT2.evaluate(0).get(tip);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("GT2 average evaluate COS time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseGT2.evaluate(1).get(tip);
            timecount += System.nanoTime() - start;
        }
        System.out.println("GT2 average evaluate Centroid time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseGT2.evaluateGetCentroid(0).get(tip);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("GT2 average evaluate COS getCentroid time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            rulebaseGT2.evaluateGetCentroid(1).get(tip);
            timecount += System.nanoTime() - start;
        }
        System.out.println("GT2 average evaluate Centroid getCentroid time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
    }

    public void getRulebaseGT2MulticoreTimes(){
        FLC = new FLCPoolFactory(rulebaseGT2.getIT2Rulebases());
        food.setInput(foodIn);
        service.setInput(serviceIn);
        long timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            FLC.runFactory(0).get(tip);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("GT2 average evaluate COS time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            FLC.runFactory(1).get(tip);
            timecount += System.nanoTime() - start;
        }
        System.out.println("GT2 average evaluate Centroid time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            FLC.runFactoryGetCentroid(0).get(tip);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("GT2 average evaluate COS getCentroid time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            FLC.runFactoryGetCentroid(1).get(tip);
            timecount += System.nanoTime() - start;
        }
        System.out.println("GT2 average evaluate Centroid getCentroid time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
    }

    public void getPlotTimes(){
        long timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotMFT1("Test", new T1MF_Interface[]{badFoodUMF,greatFoodUMF}, food.getDomain(), 100);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("plotMF (T1) average time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotMFIT2("Test", new IntervalT2MF_Interface[]{badFoodIT2MF,greatFoodIT2MF}, 100);
            timecount += System.nanoTime() - start;
        }
        System.out.println("plotMF2 (IT2) average time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotMFGT2("Test", new GenT2zMF_Interface[]{badFoodMF,greatFoodMF},food.getDomain(), 100,true,false);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("plotMFasLines (GT2) average time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotMFGT2("Test", new GenT2zMF_Interface[]{badFoodMF,greatFoodMF},food.getDomain(), 100,false,true);
            timecount += System.nanoTime() - start;
        }
        System.out.println("plotMFasSurface (GT2) average time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");

    }

    public void getControlSurfaceTimes(){
        long timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotControlSurface(true, xDiscs, yDiscs);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("ControlSurfaceData GT2 Centroid average time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotControlSurface(false, xDiscs, yDiscs);
            timecount += System.nanoTime() - start;
        }
        System.out.println("ControlSurfaceData GT2 COS average time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotControlSurfaceMC(true, xDiscs, yDiscs);
            timecount += System.nanoTime() - start;
            //System.out.println(System.currentTimeMillis());
        }
        //long seconds = TimeUnit.NANOSECONDS.toSeconds(timecount/count);
        System.out.println("ControlSurfaceData GT2 Centroid Multicore average time over " + count + " iterations is "+(timecount/count)+ " nano seconds.");
        timecount = 0;
        for(int i=0;i<count;i++){
            long start = System.nanoTime();
            plotControlSurfaceMC(false, xDiscs, yDiscs);
            timecount += System.nanoTime() - start;
        }
        System.out.println("ControlSurfaceData GT2 COS Multicore average time over " + count + " iterations is "+ (timecount/count)+ " nano seconds.");
    }

    private void plotMFT1(String name, T1MF_Interface[] sets, Tuple xAxisRange, int discretizationLevel)
    {
        JMathPlotter plotter = new JMathPlotter(17,17,15);
        for (int i=0;i<sets.length;i++)
        {
            plotter.plotMF(sets[i].getName(), sets[i], discretizationLevel, xAxisRange, new Tuple(0.0,1.0),false);
        }
        //plotter.show(name);
    }

    private void plotMFIT2(String name, IntervalT2MF_Interface[] sets, int discretizationLevel)
    {
        JMathPlotter plotter = new JMathPlotter();
        plotter.plotMF(sets[0].getName(), sets[0], discretizationLevel, null, true);
       
        for (int i=1;i<sets.length;i++)
        {
            plotter.plotMF(sets[i].getName(), sets[i], discretizationLevel, null, true);
        }
        //plotter.show(name);
    }

    private void plotMFGT2(String name, GenT2zMF_Interface[] sets, Tuple xAxisRange, int discretizationLevel, boolean plotAsLines, boolean plotAsSurface)
    {
        if(plotAsLines)
        {
            JMathPlotter plotter = new JMathPlotter();
            plotter.plotMFasLines(sets[0].getName(), sets[0], discretizationLevel);

            for (int i=1;i<sets.length;i++)
            {
                plotter.plotMFasLines(sets[i].getName(), sets[i], discretizationLevel);
            }
            //plotter.show(name);
        }
        if(plotAsSurface)
        {
            JMathPlotter plotterSurf = new JMathPlotter();
            plotterSurf.plotMFasSurface(sets[0].getName(), sets[0], xAxisRange, discretizationLevel,false);

            for (int i=1;i<sets.length;i++)
            {
                plotterSurf.plotMFasSurface(sets[i].getName(), sets[i], xAxisRange, discretizationLevel, false);
            }
            //plotterSurf.show(name);
        }        
    }
        
    private void plotControlSurface(boolean useCentroidDefuzzification, int input1Discs, int input2Discs)
    {
        double output;
        double[] x = new double[input1Discs];
        double[] y = new double[input2Discs];
        //double[][] z = new double[x.length][y.length];
        double[][] z = new double[y.length][x.length];
        double incrX, incrY;
        incrX = food.getDomain().getSize()/(input1Discs-1.0);
        incrY = service.getDomain().getSize()/(input2Discs-1.0);

        //first, get the values
        for(int currentX=0; currentX<input1Discs; currentX++)
        {
            x[currentX] = currentX * incrX;        
        }
        for(int currentY=0; currentY<input2Discs; currentY++)
        {
            y[currentY] = currentY * incrY;
        }
        
        for(int currentX=0; currentX<input1Discs; currentX++)
        {
            food.setInput(x[currentX]);
            for(int currentY=0; currentY<input2Discs; currentY++)
            {
                service.setInput(y[currentY]);
                if(useCentroidDefuzzification)
                    output = rulebaseGT2.evaluate(1).get(tip);
                else
                    output = rulebaseGT2.evaluate(0).get(tip);
                
                //System.out.println("Current x = "+currentX+"  current y = "+currentY+"  output = "+output);
                z[currentY][currentX] = output;
            }    
        }
      
    }

    private void plotControlSurfaceMC( boolean useCentroidDefuzzification, int input1Discs, int input2Discs)
    {
        FLC = new FLCPoolFactory(rulebaseGT2.getIT2Rulebases());
        double output;
        double[] x = new double[input1Discs];
        double[] y = new double[input2Discs];
        //double[][] z = new double[x.length][y.length];
        double[][] z = new double[y.length][x.length];
        double incrX, incrY;
        incrX = food.getDomain().getSize()/(input1Discs-1.0);
        incrY = service.getDomain().getSize()/(input2Discs-1.0);

        //first, get the values
        for(int currentX=0; currentX<input1Discs; currentX++)
        {
            x[currentX] = currentX * incrX;        
        }
        for(int currentY=0; currentY<input2Discs; currentY++)
        {
            y[currentY] = currentY * incrY;
        }
        
        for(int currentX=0; currentX<input1Discs; currentX++)
        {
            food.setInput(x[currentX]);
            for(int currentY=0; currentY<input2Discs; currentY++)
            {
                service.setInput(y[currentY]);
                if(useCentroidDefuzzification)
                    output = FLC.runFactory(1).get(tip);
                else
                    output = FLC.runFactory(0).get(tip);
                
                z[currentY][currentX] = output;
            }    
        }
        
    }  

    public static void main (String args[])
    {
        test t =  new test();
        t.setup();
        System.out.println("-------- GT2 Multicore --------");
        t.getRulebaseGT2MulticoreTimes();
        System.out.println("------------- GT2 -------------");
        t.getRulebaseGT2Times();
        System.out.println("------------- IT2 -------------");
        t.getRulebaseIT2Times();
        System.out.println("------------- T1 --------------");
        t.getRulebaseT1Times();
        System.out.println("------------ Plot -------------");
        t.getPlotTimes();
        System.out.println("------- Control Surface -------");
        t.getControlSurfaceTimes();
    }
  
}
