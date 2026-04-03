clear;
close all;
clc;

%% fprintf() is a function that allows you to print formatted data to the command window.
a = 1;
fprintf('%d\n',a);

%% Different ways to display the matrix A as an image
A = 1*[[1,145];
     [212,355]];

% 1. Using imshow(A) with default settings, displaying only [0,1] values
figure;
subplot(1,3,1);
imshow(A);
set(gca, 'YDir', 'normal')
colormap("gray");
colorbar;

% 2. Using imshow(A,[]) to display the full range of values in A
subplot(1,3,2);
imshow(A, []);
set(gca, 'YDir', 'normal')
colormap("gray");
colorbar;


% 3. Using imagesc(A) to display the full range of values in A
subplot(1,3,3);
imagesc(A);
set(gca, 'YDir', 'normal')
axis equal tight;
colormap("gray");
colorbar;
