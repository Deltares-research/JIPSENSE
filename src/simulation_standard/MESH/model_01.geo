// square
lc=0.1;
lc0 = 0.25;
lc1 = 0.25;

h = 30.0;
l = 100.0;
d_sand = h-3;
d_sed = d_sand + 0.5;


//BOX
Point(1) = {0, 0, 0, lc0};
Point(2) = {l, 0 , 0, lc0};
Point(3) = {l, h, 0, lc1};
Point(4) = {0, h, 0, lc1};

//Interior points

Point(5) = {0, d_sand, 0, lc};
Point(6) = {l, d_sand, 0, lc};

Point(7) = {0, d_sed, 0, lc};
Point(8) = {l, d_sed, 0, lc};


// ########### drawing lines ##########

// Bottom edge
Line(100) = {1,2};

// Right edge
Line(101) = {2,6};
Line(102) = {6,8};
Line(103) = {8,3};


// Top edge
Line(104) = {3,4};

// Left edge
Line(105) = {4,7};
Line(106) = {7,5};
Line(107) = {5,1};

// water/sediment interface
Line(108) = {7,8};

// sediment/sand interface
Line(109) = {5,6};

// create layers
// Water layer
Line Loop(1000) = {108,103,104,105};
Plane Surface(1) = {1000};

// Soft sediment layer
Line Loop(2000) = {109,102,-108,106};
Plane Surface(2) = {2000};

// Sand layer
Line Loop(3000) = {100,101,-109,107};
Plane Surface(3) = {3000};

// Combine layers
Recombine Surface{1,2,3};

// meshing
// quads mesh
//Mesh.SubdivisionAlgorithm = 1;
//Mesh.ElementOrder = 1;

// Delimite boundaries

Physical Line("Top") = {104};
Physical Line("Left") = {105,106,107};
Physical Line("Bottom") = {100};
Physical Line("Right") = {101,102,103};
Physical Surface("M1") = {1};
Physical Surface("M2") = {2};
Physical Surface("M3") = {3};

