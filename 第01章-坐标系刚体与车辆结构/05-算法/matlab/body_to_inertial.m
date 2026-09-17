function pI = body_to_inertial(origin, psi, p_body)
pI = origin(:) + rot2(psi) * p_body(:);
end
