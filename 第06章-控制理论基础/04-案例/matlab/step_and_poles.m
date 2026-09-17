thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));

dt = 0.001; T = 5; n = round(T/dt); t = linspace(0,T,n+1);
wn = 4; zetas = [0.3, 0.7, 1.2]; styles = {'-', '--', ':'};
figure; hold on;
for i = 1:3
    zeta = zetas(i); y = 0; yd = 0; ys = zeros(1,n+1);
    for k = 1:n
        ydd = wn^2*(1-y) - 2*zeta*wn*yd;
        yd = yd + dt*ydd; y = y + dt*yd; ys(k+1) = y;
    end
    plot(t, ys, ['k' styles{i}]);
end
grid on; xlabel('t (s)'); ylabel('y'); legend('0.3','0.7','1.2');
title('Second-order step response');

for vx = [10 20 30]
    A = lateral_AB(vx);
    disp(vx); disp(eig(A).');
end
