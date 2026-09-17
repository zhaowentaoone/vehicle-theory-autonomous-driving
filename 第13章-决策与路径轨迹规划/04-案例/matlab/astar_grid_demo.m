thisDir = fileparts(mfilename('fullpath'));
root = fileparts(fileparts(fileparts(thisDir)));
addpath(fullfile(root, 'common', 'matlab'));
grid = zeros(30,30);
grid(6:25, 13:16) = 1;
grid(19:22, 17:24) = 1;
start = [3,3]; goal = [28,28];
[path, expanded] = astar_grid(grid, start, goal);
fprintf('path=%d expanded=%d\n', size(path,1), expanded);
figure; imagesc(grid); set(gca,'YDir','normal'); colormap(gray); hold on;
if ~isempty(path), plot(path(:,2), path(:,1), 'k-o'); end
plot(start(2), start(1), 'gs', goal(2), goal(1), 'rs');
title('A* on occupancy grid');
