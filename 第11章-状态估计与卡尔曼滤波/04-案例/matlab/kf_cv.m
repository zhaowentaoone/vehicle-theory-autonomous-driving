thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
rng(0);
dt = 0.05; A = [1 dt; 0 1]; C = [1 0];
Q = diag([0.01, 0.8])*dt; R = 4;
T = 20; n = round(T/dt);
p_true = 0; v_true = 10;
x = [0; 8]; P = diag([10, 10]);
ts = linspace(0,T,n);
rec = zeros(n,5);
for k = 1:n
    if ts(k) >= 8, v_true = 16; end
    p_true = p_true + dt*v_true;
    y = p_true + 2*randn;
    [x,P] = kf_predict(x,P,A,Q);
    [x,P] = kf_update(x,P,y,C,R);
    rec(k,:) = [p_true, v_true, y, x(1), x(2)];
end
fprintf('pos RMSE meas=%.3f kf=%.3f\n', rms(rec(:,3)-rec(:,1)), rms(rec(:,4)-rec(:,1)));
figure;
subplot(2,1,1); plot(ts, rec(:,3), '.', ts, rec(:,1), 'k--', ts, rec(:,4), 'k-'); grid on; legend('meas','true','kf');
subplot(2,1,2); plot(ts, rec(:,2), 'k--', ts, rec(:,5), 'k-'); grid on; legend('true v','kf v');
sgtitle('Constant-velocity Kalman filter');
