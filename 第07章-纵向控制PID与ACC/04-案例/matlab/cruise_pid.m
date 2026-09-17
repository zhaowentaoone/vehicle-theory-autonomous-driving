dt = 0.01; T = 15; n = round(T/dt);
st.kp = 0.8; st.ki = 0.25; st.kd = 0; st.umin = -4; st.umax = 2;
st.I = 0; st.e_prev = 0;
v = 10; a = 0; tau = 0.3;
ts = linspace(0,T,n+1); vs = zeros(1,n+1); refs = vs; vs(1)=v;
for k = 1:n
    vref = 15; if ts(k) >= 4, vref = 25; end
    refs(k) = vref;
    [ades, st] = pid_step(vref-v, dt, st);
    a = a + dt*(ades-a)/tau;
    v = v + dt*a;
    vs(k+1) = v;
end
refs(end)=refs(end-1);
figure; plot(ts,vs,'k-', ts,refs,'k--'); grid on;
xlabel('t (s)'); ylabel('m/s'); title('Cruise PI'); legend('v','v_{ref}');
