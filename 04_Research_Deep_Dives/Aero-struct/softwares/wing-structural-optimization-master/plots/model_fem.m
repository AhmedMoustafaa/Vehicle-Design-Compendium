L = data.critic_cond.L(end/2+1:end)*1.5*1.15;
Mt_p = data.critic_cond.Ma(end/2+1:end)*1.5*1.15;

xl = [data.props.centroide];
xl = xl(1:2:end);

Mt_delta = L .* xl;

Mt = Mt_p + Mt_delta;

s = data.critic_cond.x(end/2+1:end);

plot(s,Mt_p,'-o');hold on;
plot(s,Mt,'-o');

mt_1 = cumsum(flip(Mt_p));
mt_2 = cumsum(flip(Mt));
figure;
plot(s,mt_1,'-o');hold on;
plot(s,mt_2,'-o');

model.s = s*1e3;
model.Mt = -Mt*1e3;
model.L = L;
model.s_fuselagem = data.desenho.fuselagem*1e3;

clearvars L Mt_p xl Mt_delta Mt s mt_1 mt_2