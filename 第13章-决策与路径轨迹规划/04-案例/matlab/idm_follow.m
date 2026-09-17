thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
dt = 0.02; T = 25; n = round(T/dt);
v = 18; vp = 20; s = 40;
t = linspace(0,T,n+1);
vs = zeros(1,n+1); vps = vs; ss = vs;
vs(1)=v; vps(1)=vp; ss(1)=s;
for k = 1:n
    if t(k) < 10, ap = 0; elseif vp > 2, ap = -3; else, ap = 0; end
    a = idm_accel(v, vp, s);
    v = max(v + dt*a, 0);
    vp = max(vp + dt*ap, 0);
    s = max(s + dt*(vp-v), 0.1);
    vs(k+1)=v; vps(k+1)=vp; ss(k+1)=s;
end
fprintf('min spacing = %.2f m\n', min(ss));
figure;
subplot(2,1,1); plot(t,vs,'k-', t,vps,'k--'); grid on; legend('ego','lead');
subplot(2,1,2); plot(t,ss,'k-'); grid on; ylabel('spacing'); xlabel('t');
sgtitle('IDM car-following');
