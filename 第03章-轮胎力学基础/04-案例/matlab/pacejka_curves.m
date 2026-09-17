thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));

B = 8; C = 1.25; D = 8000; E = 0.4;
alpha_deg = linspace(-15, 15, 400);
alpha = deg2rad(alpha_deg);
Fy = pacejka(alpha, B, C, D, E);
slope = B*C*D;
Fy_lin = slope * alpha;
sigma = linspace(-0.2, 0.2, 400);
Fx = pacejka(sigma, B, C, D, E);

[~, ip] = max(Fy);
fprintf('BCD = %.0f N/rad, peak Fy = %.0f N at %.2f deg\n', slope, Fy(ip), alpha_deg(ip));

figure;
subplot(1,2,1);
plot(alpha_deg, Fy, 'k-', alpha_deg, Fy_lin, 'k--');
xlabel('alpha (deg)'); ylabel('Fy (N)'); title('Pure cornering'); grid on;
legend('Pacejka', 'linear BCD*alpha'); ylim([-9000 9000]);
subplot(1,2,2);
plot(sigma, Fx, 'k-');
xlabel('longitudinal slip sigma'); ylabel('Fx (N)'); title('Pure longitudinal'); grid on;
