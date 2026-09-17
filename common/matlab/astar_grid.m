function [path, expanded] = astar_grid(grid, start, goal)
[h, w] = size(grid);
nbrs = [-1 0; 1 0; 0 -1; 0 1; -1 -1; -1 1; 1 -1; 1 1];
g = inf(h,w); g(start(1), start(2)) = 0;
came = zeros(h,w,2);
in_open = false(h,w);
open = [heuristic(start,goal), start];
expanded = 0;
closed = false(h,w);
while ~isempty(open)
    [~, idx] = min(open(:,1));
    cur = open(idx, 2:3); open(idx,:) = [];
    if closed(cur(1), cur(2)), continue; end
    closed(cur(1), cur(2)) = true;
    expanded = expanded + 1;
    if isequal(cur, goal)
        path = cur;
        while any(came(cur(1),cur(2),:))
            cur = squeeze(came(cur(1),cur(2),:))';
            path = [cur; path]; %#ok<AGROW>
        end
        return;
    end
    for k = 1:8
        nb = cur + nbrs(k,:);
        if nb(1)<1 || nb(1)>h || nb(2)<1 || nb(2)>w || grid(nb(1),nb(2))==1
            continue;
        end
        tg = g(cur(1),cur(2)) + hypot(nbrs(k,1), nbrs(k,2));
        if tg < g(nb(1),nb(2))
            g(nb(1),nb(2)) = tg;
            came(nb(1),nb(2),:) = cur;
            open(end+1,:) = [tg + heuristic(nb,goal), nb]; %#ok<AGROW>
        end
    end
end
path = [];
end

function d = heuristic(a, b)
d = hypot(a(1)-b(1), a(2)-b(2));
end
