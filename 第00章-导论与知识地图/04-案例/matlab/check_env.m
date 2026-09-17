% 第00章：MATLAB 环境自检
fprintf('MATLAB %s\n', version);
t = linspace(0, 1, 50);
y = 2 * t + 0.5;
figure;
plot(t, y, 'k-');
xlabel('t (s)');
ylabel('y');
title('Ch00 env check: a straight line');
grid on;
fprintf('MATLAB graphics OK\n');
