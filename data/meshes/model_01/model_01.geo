// Gmsh geometry file: model_01

lc = 0.15;
lc0 = 0.15;
lc1 = 0.15;
h = 3.0;
l = 30.0;
d_sand = 0.5;

// Points
Point(1) = {0, 0, 0, 0.15};
Point(2) = {30.0, 0, 0, 0.15};
Point(3) = {30.0, 3.0, 0, 0.15};
Point(4) = {0, 3.0, 0, 0.15};
Point(5) = {0, 0.5, 0, 0.15};
Point(6) = {30.0, 0.5, 0, 0.15};

// Lines
Line(100) = {1, 2};
Line(101) = {2, 6};
Line(102) = {6, 3};
Line(103) = {3, 4};
Line(104) = {4, 5};
Line(105) = {5, 1};
Line(106) = {5, 6};

// Surfaces & Line Loops
Line Loop(1) = {106, 102, 103, 104};
Plane Surface(1) = {1};
Line Loop(2) = {100, 101, -106, 105};
Plane Surface(2) = {2};

// Mesh settings
Recombine Surface{1, 2};
Mesh.SubdivisionAlgorithm = 1;
Mesh.ElementOrder = 1;

// Physical boundaries
Physical Line("Top") = {103};
Physical Line("Bottom") = {100};
Physical Line("Left") = {104, 105};
Physical Line("Right") = {101, 102};

// Physical surfaces (materials)
Physical Surface("M1") = {1};
Physical Surface("M2") = {2};