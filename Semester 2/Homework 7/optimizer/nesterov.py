import numpy as np
from .optimizer import OptimMeta

class NesterovOptim(OptimMeta, format_name='Nesterov'):
    def __iter__(self):
        return self

    def set_parameters(self, f_grad, x_start, lr=0.01, eps=1e-8, n_iterations=500, **kwargs):
        self.x = x_start.copy()
        self.v = np.zeros_like(self.x)
        self.f_grad = f_grad
        self.cur_iter = 0
        self.n_iter = n_iterations
        self.eps = eps
        self.lr = lr
        self.mu = kwargs.get('mu', 0.9)
        return self

    def __next__(self):
        if self.cur_iter >= self.n_iter:
            raise StopIteration
        grad = self.f_grad(self.x + self.mu * self.v)
        if np.linalg.norm(grad) < self.eps:
            raise StopIteration
        self.v = self.mu * self.v - self.lr * grad
        self.x = self.x + self.v
        self.cur_iter += 1
        return self.x