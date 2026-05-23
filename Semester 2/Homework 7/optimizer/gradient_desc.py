import numpy as np
from .optimizer import OptimMeta

class GDOptim(OptimMeta, format_name='GD'):
    def __iter__(self):
        return self

    def set_parameters(self, f_grad, x_start, lr=0.01, eps=1e-8, n_iterations=500, **kwargs):
        self.x = x_start.copy()
        self.f_grad = f_grad
        self.cur_iter = 0
        self.n_iter = n_iterations
        self.eps = eps
        self.lr = lr
        return self

    def __next__(self):
        if self.cur_iter >= self.n_iter:
            raise StopIteration
        grad = self.f_grad(self.x)
        if np.linalg.norm(grad) < self.eps:
            raise StopIteration
        self.x -= self.lr * grad
        self.cur_iter += 1
        return self.x