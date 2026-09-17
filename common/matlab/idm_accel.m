function a = idm_accel(v, vp, s, v0, T, amax, b, s0)
if nargin < 8, s0 = 4; end
if nargin < 7, b = 2; end
if nargin < 6, amax = 1.4; end
if nargin < 5, T = 1.4; end
if nargin < 4, v0 = 25; end
dv = v - vp;
s_star = s0 + max(0, v*T + v*dv/(2*sqrt(amax*b)));
a = amax * (1 - (v/max(v0,0.1))^4 - (s_star/max(s,0.2))^2);
a = max(min(a, amax), -6);
end
