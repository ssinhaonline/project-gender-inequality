function myheatmap(mymat)

xlab = {'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'};
ylab = {'1 - 1.5','1.5 - 2','2 - 2.5','2.5 - 3','3 - 3.5','3.5 - 4','4 - 4.5','4.5 - 5'};
xticks = [1 2 3 4 5 6 7 8 9 10 11 12];
figureh = figure;
axesh = axes('Parent', figureh);
hold(axesh, 'on');
set(axesh, 'XTick', xticks, 'XTickLabel', xlab, 'YTickLabel', ylab);
xlim(axesh,[0.5 12.5]);
ylim(axesh,[0.5 8.5]);
int_t = transpose(mymat);
colormap('jet');
imagesc(int_t);
caxis manual
caxis([9000 250000]);
colorbar;