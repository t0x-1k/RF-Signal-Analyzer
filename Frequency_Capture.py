import numpy as np
import matplotlib.pyplot as plt
from rtlsdr import RtlSdr
import pyvista as pv
from pyvista import Plotter
import time


def initialize_sdr() -> RtlSdr:
    sdr = RtlSdr()
    sdr.sample_rate = 2.048e6
    sdr.center_freq = 100e6
    sdr.freq_correction = 60
    sdr.gain = 'auto'
    return sdr


def create_grid(grid_size: int, sample_rate: float, y_depth: float, z_scale: float) -> pv.StructuredGrid:
    x = np.linspace(-sample_rate / 2, sample_rate / 2, grid_size)
    y = np.linspace(0, y_depth, grid_size)
    z = np.zeros(grid_size * grid_size)

    xx, yy = np.meshgrid(x, y)
    points = np.column_stack((xx.ravel(), yy.ravel(), z))

    grid = pv.StructuredGrid()
    grid.points = points
    grid.dimensions = (grid_size, grid_size, 1)
    return grid


def update_fft_grid(grid: pv.StructuredGrid, samples: np.ndarray, z_scale: float) -> None:
    fft_size = len(samples)
    window = np.blackman(fft_size)
    fft_result = np.fft.rfft(window * samples)
    fft_power = 10 * np.log10(np.abs(fft_result)**2 / fft_size + 1e-12)  # avoid log(0)

    z_values = np.tile(fft_power[:grid.dimensions[0]] * z_scale, grid.dimensions[1])
    grid.points[:, 2] = z_values


def main_loop(grid_size: int = 100, z_scale: float = 1e-6, refresh_rate: float = 0.5) -> None:
    sdr = initialize_sdr()
    plotter = Plotter()
    plotter.set_background('black')

    grid = create_grid(grid_size, sdr.sample_rate, y_depth=10, z_scale=z_scale)
    mesh = plotter.add_mesh(grid, cmap="viridis", scalars=grid.points[:, 2], show_scalar_bar=True)
    plotter.show(auto_close=False)

    try:
        print("🔄 Starting real-time FFT capture. Press Ctrl+C to stop.")
        while True:
            samples = sdr.read_samples(256 * 1024)
            update_fft_grid(grid, samples, z_scale)
            mesh.points = grid.points  # Efficient way to update mesh
            plotter.update()
            time.sleep(refresh_rate)
    except KeyboardInterrupt:
        print("🛑 Interrupted by user, shutting down.")
    finally:
        sdr.close()
        plotter.close()
        grid.save("rf_capture.obj")


if __name__ == "__main__":
    main_loop()
