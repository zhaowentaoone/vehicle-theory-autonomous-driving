dt = 0.01; T = 25; n = round(T/dt);
h = 1.4; s0 = 5; Ks = 0.25; Kv = 0.9;
v = 18; vp = 20; s = 40;
t = linspace(0,T,n+1);
ss = zeros(1,n+1); vs = ss; vps = ss;
ss(1)=s; vs(1)=v; vps(1)=vp;
for k = 1:n
    if t(k) < 8, ap = 0; elseif vp > 10, ap = -2; else, ap = 0; end
    sdes = s0 + h*v;
    acc = Ks*(s-sdes) + Kv*(vp-v);
    acc = max(min(acc,2),-5);
    v = max(v + dt*acc, 0);
    vp = max(vp + dt*ap, 0);
    s = s + dt*(vp-v);
    ss(k+1)=s; vs(k+1)=v; vps(k+1)=vp;
end
fprintf('min spacing = %.2f m\n', min(ss));
figure;
subplot(2,1,1); plot(t,vs,'k-', t,vps,'k--'); grid on; legend('ego','lead'); ylabel('m/s');
subplot(2,1,2); plot(t,ss,'k-', t,s0+h*vs,'k--'); grid on; ylabel('m'); xlabel('t (s)');
sgtitle('ACC constant time-gap');
