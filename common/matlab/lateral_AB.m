function [A, B] = lateral_AB(vx, p)
if nargin < 2
    p = vehicle_params();
end
vx = max(vx, 1);
A = [-(p.Cf+p.Cr)/(p.m*vx), -vx-(p.Cf*p.lf-p.Cr*p.lr)/(p.m*vx);
     -(p.Cf*p.lf-p.Cr*p.lr)/(p.Iz*vx), -(p.Cf*p.lf^2+p.Cr*p.lr^2)/(p.Iz*vx)];
B = [p.Cf/p.m; p.Cf*p.lf/p.Iz];
end
