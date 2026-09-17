function [u, st] = pid_step(e, dt, st)
st.I = st.I + e * dt;
d = (e - st.e_prev) / max(dt, eps);
u = st.kp * e + st.ki * st.I + st.kd * d;
u_sat = max(st.umin, min(st.umax, u));
if u ~= u_sat
    st.I = st.I - e * dt;
end
st.e_prev = e;
u = u_sat;
end
