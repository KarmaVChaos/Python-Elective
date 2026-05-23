import numpy as np
from .optimizer import OptimMeta

class AdamOptim(OptimMeta, format_name='Adam'):
    def __iter__(self):
        return self

    def set_parameters(self, f_grad, x_start, lr=0.01, eps=1e-8, n_iterations=500, **kwargs):
        self.x = x_start.copy()
        self.v = np.zeros_like(self.x)
        self.m = np.zeros_like(self.x)
        self.f_grad = f_grad
        self.cur_iter = 1
        self.n_iter = n_iterations
        self.eps = eps
        self.lr = lr
        self.beta = kwargs.get('beta', 0.9)
        self.beta2 = kwargs.get('beta2', 0.999)
        return self

    def __next__(self):
        if self.cur_iter > self.n_iter:
            raise StopIteration
        grad = self.f_grad(self.x)
        if np.linalg.norm(grad) < self.eps:
            raise StopIteration

        self.m = self.beta * self.m + (1 - self.beta) * grad
        self.v = self.beta2 * self.v + (1 - self.beta2) * (grad ** 2)

        m_hat = self.m / (1 - self.beta ** self.cur_iter)
        v_hat = self.v / (1 - self.beta2 ** self.cur_iter)

        self.x -= self.lr * m_hat / (np.sqrt(v_hat) + self.eps)
        self.cur_iter += 1
        return self.x