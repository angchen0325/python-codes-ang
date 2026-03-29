clear;
close all;
clc;

a = 1;
fprintf('%d\n',a);

A = 1*[[1,2];
     [3,4]];


figure;
subplot(1,3,1);
imshow(A);
colormap("gray");
colorbar;

subplot(1,3,2);
imshow(A, []);
colormap("gray");
colorbar;

subplot(1,3,3);
imagesc(A);
axis equal tight;
colormap("gray");
colorbar;
