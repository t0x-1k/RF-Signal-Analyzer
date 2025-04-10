import numpy as np
import pyvista as pv
import matplotlib.pyplot as plt

def simulate_signal_strength():
    """Simulates and visualizes 3D signal strength based on processor and RF parameters."""

    # Configuration block
    config = {
        "power_watts": 100,
        "surface_area": 0.1,
        "clock_speed": 64e6,
        "program_mem_size": 128_000,
        "data_mem_size": 1_536,
        "utilization": 0.65,
        "frequency_start": 2e14,
        "frequency_end": 4e14,
        "frequency_points": 500,
    }

    # Apply utilization adjustments
    clock_speed = config["clock_speed"] * config["utilization"]
    power_watts = config["power_watts"] * config["utilization"]
    power_density_sq = power_watts / config["surface_area"]
    
    freq_range = np.linspace(config["frequency_start"], config["frequency_end"], config["frequency_points"])
    gain = np.full(freq_range.shape, 10)
    noise_level = np.sqrt(freq_range) / 1000
    power_consumption = np.random.uniform(50, 200, size=freq_range.shape) * config["utilization"]

    # 3D signal strength simulation grid
    linspace = np.linspace(0, 100, 20)
    X, Y, Z = np.meshgrid(linspace, linspace, linspace, indexing='ij')
    distances = np.linalg.norm(np.stack((X, Y, Z)), axis=0)
    signal_strength = (1 / (distances + 1)) * config["utilization"]

    points = np.stack((X, Y, Z), axis=-1).reshape(-1, 3)
    signal_strength_flat = signal_strength.ravel()

    # Visualization
    plotter = pv.Plotter(notebook=False)
    plotter.set_background('white')
    plotter.add_mesh(points, scalars=signal_strength_flat, cmap="viridis",
                     point_size=10, render_points_as_spheres=True, opacity=[0.0, 0.6])
    plotter.camera_position = [(150, 150, 150), (50, 50, 50), (0, 0, 1)]
    plotter.show(auto_close=False)

    depth_image = plotter.get_image_depth()
    plotter.close()

    # Depth image plot
    plt.figure(figsize=(10, 8))
    plt.imshow(depth_image, cmap='gray')
    plt.colorbar(label='Depth')
    plt.title('Depth Image')
    plt.xlabel('X-axis')
    plt.ylabel('Y-axis')
    plt.show()

    # Output metadata (optional for debug/logging)
    device_levels = {
        "power_density_sq": power_density_sq,
        "gain": gain,
        "noise_level": noise_level,
        "power_consumption": power_consumption,
        "power_watts": power_watts,
        "surface_area": config["surface_area"],
        "clock_speed": clock_speed,
        "program_mem_size": config["program_mem_size"],
        "data_mem_size": config["data_mem_size"]
    }

    return device_levels

# Example usage
if __name__ == "__main__":
    metadata = simulate_signal_strength()
    print("Simulation complete. Metadata summary:")
    for key, value in metadata.items():
        print(f"{key}: {value if isinstance(value, (int, float)) else 'array'}")
