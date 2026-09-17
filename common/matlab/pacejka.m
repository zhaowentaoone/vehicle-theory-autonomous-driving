function F = pacejka(kappa, B, C, D, E)
x = B * kappa;
F = D * sin(C * atan(x - E * (x - atan(x))));
end
