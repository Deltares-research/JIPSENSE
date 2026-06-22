// square
lc=0.3;
lc0 = 0.25;
lc1 = 0.3;

h = 3.0;
l = 30.0;
d_sand = 0.5;


//BOX
Point(1) = {0, 0, 0, lc0};
Point(2) = {l, 0 , 0, lc0};
Point(3) = {l, h, 0, lc1};
Point(4) = {0, h, 0, lc1};

//Interior points

Point(5) = {0, d_sand, 0, lc};
Point(6) = {l, d_sand, 0, lc};


// ########### drawing lines ##########

// Bottom edge
Line(100) = {1,2};

// Right edge
Line(101) = {2,6};
Line(102) = {6,3};

// Top edge
Line(103) = {3,4};

// Left edge
Line(104) = {4,5};
Line(105) = {5,1};

// water/sand interface
Line(106) = {5,6};

// create layers
// Water layer
Line Loop(1000) = {106,102,103,104};
Plane Surface(1) = {1000};

// Soft sediment layer
Line Loop(2000) = {100,101,-106,105};
Plane Surface(2) = {2000};


// Combine layers
Recombine Surface{1,2};

// meshing
// quads mesh
Mesh.SubdivisionAlgorithm = 1;
Mesh.ElementOrder = 1;

// Delimite boundaries

Physical Line("Top") = {103};
Physical Line("Left") = {104,105};
Physical Line("Bottom") = {100};
Physical Line("Right") = {101,102};
Physical Surface("M1") = {1};
Physical Surface("M2") = {2};

