function p = vehicle_params()
% 教学用紧凑型轿车参数。全书 MATLAB 案例默认调用本函数。
p.m   = 1500;
p.Iz  = 2250;
p.lf  = 1.2;
p.lr  = 1.6;
p.L   = p.lf + p.lr;
p.Cf  = 80000;
p.Cr  = 80000;
p.Re  = 0.30;
p.Cd  = 0.30;
p.Af  = 2.2;
p.rho = 1.225;
p.fr  = 0.015;
p.g   = 9.81;
end
