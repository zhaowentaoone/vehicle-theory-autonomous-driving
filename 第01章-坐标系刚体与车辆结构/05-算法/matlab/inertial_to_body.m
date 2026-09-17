function pB = inertial_to_body(origin, psi, p_inertial)
pB = rot2(psi)' * (p_inertial(:) - origin(:));
end
