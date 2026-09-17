% 车体系矩形、轴心 → 惯性系并绘图
thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
p = vehicle_params();

origin = [0, 0];
psi_deg = 35;
psi = deg2rad(psi_deg);
R = [cos(psi), -sin(psi); sin(psi), cos(psi)];

length = 4.5; width = 1.8;
hl = length/2; hw = width/2;
corners_body = [hl, hl, -hl, -hl, hl; hw, -hw, -hw, hw, hw];
corners_i = origin' + R * corners_body;
fa_i = origin' + R * [p.lf; 0];
ra_i = origin' + R * [-p.lr; 0];
heading = origin' + R * [2.5; 0];

figure;
plot(corners_i(1,:), corners_i(2,:), 'k-', 'LineWidth', 2); hold on;
plot(origin(1), origin(2), 'ko', 'MarkerFaceColor', 'k');
plot(fa_i(1), fa_i(2), 'r^', 'MarkerSize', 10, 'MarkerFaceColor', 'r');
plot(ra_i(1), ra_i(2), 'bs', 'MarkerSize', 10, 'MarkerFaceColor', 'b');
quiver(origin(1), origin(2), heading(1)-origin(1), heading(2)-origin(2), 0, 'Color', [0.3 0.3 0.3]);
axis equal; grid on;
xlabel('X (m)'); ylabel('Y (m)');
title(sprintf('Body rectangle in inertial frame, psi=%.0f deg', psi_deg));
legend('body', 'CG', 'front axle', 'rear axle', 'Location', 'northwest');
