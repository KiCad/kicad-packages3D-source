APA102();
module APA102(){
  //APA102-2020
  //http://www.normandled.com/upload/201807/APA102-2020%20LED%20Datasheet.pdf
  
  //alias Adafruit Dotstar
  ovDims=[2,2,0.9];
  padDims=[0.6,0.4,0.1];
  ICDims=[1,0.8,0.1];
  mfudge=0.01; //microfudge
  ICPos=[0,0.5,0.3];
  
  //PCB
  color("darkgreen") translate([0,0,ovDims.z/6+mfudge/2]) cube([ovDims.x,ovDims.y,ovDims.z/3-mfudge],true);
  //Resin
  difference(){
    color("gold",0.5) translate([0,0,ovDims.z*0.66/2+ovDims.z/3]) cube([ovDims.x,ovDims.y,ovDims.z*0.66-mfudge],true);
    translate(ICPos) cube(ICDims+[mfudge,mfudge,mfudge],true); //substract IC cavity to make transparency work
    for (i=[-0.2765,0,0.2765]) translate([i,-0.5,0.25]) cube(0.146+mfudge,true);
  }
  //pads
  for (i=[1,-1],j=[-1,0,1])
    color("silver") translate([i*(1-padDims.x/2),j*(1-padDims.y/2),padDims.z/2]) cube(padDims+[mfudge,mfudge,0],true);
  for (j=[1,-1])
    color("silver") translate([0,j*(1-0.5/2),padDims.z/2]) cube([0.3+mfudge,0.5+mfudge,padDims.z],true);
  //IC
  color("darkslategrey") translate(ICPos) cube([1,0.8,0.1],true);
  //LEDs (yes, really)
  
    color("red") translate([-0.2765,-0.5,0.25]) cube(0.146,true);
    color("green") translate([0,-0.5,0.25]) cube(0.146,true);
    color("blue") translate([0.2765,-0.5,0.25]) cube(0.146,true);
}
