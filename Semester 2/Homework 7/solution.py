import numpy as np
import cv2
import time
from scipy.ndimage import sobel, gaussian_filter
from sklearn.metrics import mean_squared_error, r2_score

def make_image(size=256, n_cells=15, cell_radius=10, noise_std=8, seed=0):
    rng = np.random.default_rng(seed)
    img = np.full((size, size), 220, dtype=np.float32)
    centers = []
    attempts = 0
    while len(centers) < n_cells and attempts < 5000:
        r = rng.integers(cell_radius, size - cell_radius)
        c = rng.integers(cell_radius, size - cell_radius)
        if all(np.hypot(r - cr, c - cc) > cell_radius * 2.5 for cr, cc in centers):
            centers.append((r, c))
            rr, cc = np.ogrid[:size, :size]
            mask = (rr - r) ** 2 + (cc - c) ** 2 <= cell_radius ** 2
            img[mask] = rng.integers(30, 80)
        attempts += 1
    img += rng.normal(0, noise_std, img.shape).astype(np.float32)
    img = np.clip(img, 0, 255)
    return img.astype(np.uint8), centers

def sobel_gradients(img, sigma=2.0):
    smooth = gaussian_filter(img.astype(np.float32), sigma=sigma)
    gy = sobel(smooth, axis=0)
    gx = sobel(smooth, axis=1)
    return gx, gy

def find_convergence(gx, gy, start_r, start_c, lr=0.5, n_iter=150):
    H, W = gx.shape
    r, c = float(start_r), float(start_c)
    for _ in range(n_iter):
        ri = int(np.clip(r, 0, H - 1))
        ci = int(np.clip(c, 0, W - 1))
        gr, gc = gy[ri, ci], gx[ri, ci]
        mag = np.hypot(gr, gc) + 1e-8
        r -= lr * gr / mag
        c -= lr * gc / mag
        r = float(np.clip(r, 0, H - 1))
        c = float(np.clip(c, 0, W - 1))
    return int(round(r)), int(round(c))

def merge_clusters(points, eps=14.0):
    clusters = []
    for p in points:
        merged = False
        for cl in clusters:
            cr, cc = cl['center']
            if np.hypot(p[0] - cr, p[1] - cc) < eps:
                cl['members'].append(p)
                n = len(cl['members'])
                cl['center'] = (sum(m[0] for m in cl['members']) / n,
                                sum(m[1] for m in cl['members']) / n)
                merged = True
                break
        if not merged:
            clusters.append({'center': (float(p[0]), float(p[1])), 'members': [p]})
    return clusters

def detect_cells(img, gx, gy, N=20, W_block=80, H_block=80, R=8,
                 lr=0.5, n_iter=150, eps_cluster=14, seed=1,
                 ref_intensity=60, intensity_tol=25):
    rng = np.random.default_rng(seed)
    H, W = img.shape
    conv_pts = []
    for _ in range(N):
        cx = rng.integers(W_block // 2, max(W - W_block // 2, W_block // 2 + 1))
        cy = rng.integers(H_block // 2, max(H - H_block // 2, H_block // 2 + 1))
        for _ in range(R):
            sr = rng.integers(cy - H_block // 2, cy + H_block // 2)
            sc = rng.integers(cx - W_block // 2, cx + W_block // 2)
            cr, cc = find_convergence(gx, gy, sr, sc, lr=lr, n_iter=n_iter)
            patch = img[max(cr-3,0):min(cr+4,H), max(cc-3,0):min(cc+4,W)]
            if patch.size > 0 and abs(patch.mean() - ref_intensity) <= intensity_tol:
                conv_pts.append((cr, cc))
    return merge_clusters(conv_pts, eps=eps_cluster), conv_pts

def _draw_histogram(values, title, color_bgr, width=300, height=200):
    canvas = np.full((height, width, 3), 240, dtype=np.uint8)
    if not values: return canvas
    counts, _ = np.histogram(values, bins=10)
    bar_w = width // 10
    max_c = max(counts) if max(counts) > 0 else 1
    for i, cnt in enumerate(counts):
        bar_h = int(cnt / max_c * (height - 30))
        cv2.rectangle(canvas, (i * bar_w + 2, height - 20 - bar_h),
                      ((i + 1) * bar_w - 2, height - 20), color_bgr, -1)
    cv2.putText(canvas, title, (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 0), 1)
    return canvas

def show_results(img, true_centers, clusters, conv_pts):
    bgr = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    p1, p2, p3 = bgr.copy(), bgr.copy(), bgr.copy()
    for r, c in true_centers: cv2.circle(p1, (c, r), 12, (0, 255, 0), 2)
    for r, c in conv_pts: cv2.circle(p2, (c, r), 2, (0, 0, 255), -1)
    for cl in clusters: cv2.circle(p3, (int(cl['center'][1]), int(cl['center'][0])), 12, (255, 255, 0), 2)
    for i, (p, t) in enumerate(zip([p1, p2, p3], ['True', 'Convergence', 'Detected'])):
        cv2.putText(p, t, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.imwrite('segmentation_result.png', np.hstack([p1, p2, p3]))
    print('segmentation_result.png saved')

def analyze_cells(img, clusters, cell_radius=12):
    stats = []
    H, W = img.shape
    for cl in clusters:
        r, c = cl['center']
        mask = np.fromfunction(lambda i,j: (i-r)**2 + (j-c)**2 <= cell_radius**2, img.shape)
        region = img[mask.astype(bool)]
        stats.append({'mean': region.mean(), 'std': region.std(),
                      'area': int(mask.sum()), 'members': len(cl['members'])})
    if not stats:
        print(' No cells detected.'); return stats
    h1 = _draw_histogram([s['mean'] for s in stats], 'Mean intensity', (200, 100, 50))
    h2 = _draw_histogram([s['std'] for s in stats], 'Std intensity', (50, 100, 200))
    h3 = _draw_histogram([s['area'] for s in stats], 'Cell area', (50, 180, 80))
    h4 = _draw_histogram([s['members'] for s in stats], 'Conv pts', (180, 50, 180))
    cv2.imwrite('eda_result.png', np.vstack([np.hstack([h1, h2]), np.hstack([h3, h4])]))
    print(' eda_result.png saved')
    return stats

def measure_quality():
    true_counts, pred_counts = [], []
    for n, seed in zip([5, 8, 10, 12, 15, 18, 20], range(7)):
        img, _ = make_image(size=256, n_cells=n, seed=seed)
        gx, gy = sobel_gradients(img)
        clusters, _ = detect_cells(img, gx, gy, N=25, W_block=80, H_block=80, R=10, seed=seed)
        true_counts.append(n); pred_counts.append(len(clusters))
    mse = mean_squared_error(true_counts, pred_counts)
    r2 = r2_score(true_counts, pred_counts)
    print(f'\n MSE={mse:.2f}, R2={r2:.3f}')
    W, H = 400, 300
    canvas = np.full((H, W, 3), 255, dtype=np.uint8)
    mn, mx = min(true_counts), max(true_counts)
    to_x = lambda v: int(30 + (v - mn) / (mx - mn + 1e-8) * (W - 60))
    to_y = lambda v: int(H - 30 - (v - mn) / (mx - mn + 1e-8) * (H - 60))
    cv2.line(canvas, (to_x(mn), to_y(mn)), (to_x(mx), to_y(mx)), (0,0,200), 1)
    for t, p in zip(true_counts, pred_counts): cv2.circle(canvas, (to_x(t), to_y(p)), 5, (200,80,0), -1)
    cv2.putText(canvas, f"MSE={mse:.2f} R2={r2:.3f}", (30, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 1)
    cv2.imwrite('quality_metric.png', canvas)
    print(' quality_metric.png saved')
    return mse, r2

def optimize_params(img, true_count, mu1=0.7, mu2=0.3, sigma_t=1.5, n_iter=10, step=2.0):
    max_F = 1.0
    def gauss(t): return np.exp(-0.5 * (t / sigma_t) ** 2)
    def objective(N, W, H, R):
        N, W, H, R = max(1, int(N)), max(10, int(W)), max(10, int(H)), max(1, int(R))
        t0 = time.perf_counter()
        gx, gy = sobel_gradients(img)
        clusters, _ = detect_cells(img, gx, gy, N=N, W_block=W, H_block=H, R=R, seed=42)
        T = time.perf_counter() - t0
        F = max(0.0, 1.0 - abs(len(clusters) - true_count) / max(true_count, 1))
        return mu1 * F / max_F + mu2 * (gauss(T) / gauss(0))

    params = np.array([15.0, 60.0, 60.0, 8.0])
    deltas = np.array([5.0, 20.0, 20.0, 3.0])
    print(f"\n Optimizing params (mu1={mu1}, mu2={mu2}):")
    for it in range(n_iter):
        f0 = objective(*params)
        grad = np.zeros(4)
        for i in range(4):
            p_plus = params.copy(); p_plus[i] += deltas[i]
            grad[i] = (objective(*p_plus) - f0) / deltas[i]
        norm = np.linalg.norm(grad) + 1e-8
        params += step * grad / norm
        params = np.clip(params, [1, 20, 20, 1], [50, 150, 150, 20])
        print(f"   iter {it+1:2d}: f={f0:.4f} | N={int(params[0])} W={int(params[1])} H={int(params[2])} R={int(params[3])}")
    print(" Optimization finished.")
    return int(round(params[0])), int(round(params[1])), int(round(params[2])), int(round(params[3]))

if __name__ == "__main__":
    print(" Generating image...")
    img, true_centers = make_image(size=256, n_cells=15, seed=42)
    true_count = len(true_centers)
    print(f"   True cells: {true_count}")

    print(" Computing gradients...")
    gx, gy = sobel_gradients(img)

    print(" Detecting cells...")
    clusters, conv_pts = detect_cells(img, gx, gy, N=25, W_block=80, H_block=80, R=10)
    print(f"   Detected: {len(clusters)}")

    show_results(img, true_centers, clusters, conv_pts)
    analyze_cells(img, clusters)
    measure_quality()
    optimize_params(img, true_count)