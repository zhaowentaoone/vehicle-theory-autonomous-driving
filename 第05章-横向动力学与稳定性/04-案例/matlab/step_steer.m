thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();
delta = deg2rad(3);
Kus = p.m/p.L*(p.lr/p.Cf - p.lf/p.Cr);
fprintf('K_us = %.4e\n', Kus);

figure;
vxs = [10, 20, 30];
styles = {'-', '--', ':'};
for i = 1:3
    vx = vxs(i); [A,B] = lateral_AB(vx, p);
    dt = 0.01; T = 5; n = round(T/dt);
    x = [0;0]; xs = zeros(2,n+1);
    for k = 1:n
        x = x + dt*(A*x + B*delta);
        xs(:,k+1) = x;
    end
    t = linspace(0,T,n+1);
    subplot(2,1,1); plot(t, rad2deg(xs(2,:)), ['k' styles{i}]); hold on;
    subplot(2,1,2); plot(t, rad2deg(xs(1,:)/vx), ['k' styles{i}]); hold on;
    fprintf('vx=%.0f steady r=%.3f beta=%.2f deg\n', vx, xs(2,end), rad2deg(xs(1,end)/vx));
end
subplot(2,1,1); ylabel('r (deg/s)'); grid on; legend('10','20','30');
subplot(2,1,2); ylabel('beta (deg)'); xlabel('t (s)'); grid on;
sgtitle('Step steer 3 deg, linear 2DOF');
