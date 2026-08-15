#!/usr/bin/env python3
"""
Beginner Example: Basic Linear Regression for Scientific Data
This example demonstrates fundamental linear regression concepts using
the Berkeley SciComp Machine Learning package. We'll analyze a simple
physics dataset and build our first predictive model.
Learning Objectives:
- Understand linear regression basics
- Learn data preprocessing steps
- Visualize model performance
- Interpret regression results
Author: Meshal Alawein
"""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys
# Add package to path
sys.path.append(str(Path(__file__).parent.parent.parent))
from Machine_Learning.supervised import LinearRegression
from Machine_Learning.utils import DataProcessor, ModelEvaluator, Visualizer
# Berkeley styling
berkeley_blue = '#003262'
california_gold = '#FDB515'
plt.style.use('seaborn-v0_8')
def create_physics_dataset():
    """
    Create a synthetic physics dataset: projectile motion.
    We'll model the relationship between launch angle and range
    for projectile motion with air resistance.
    """
    print("📊 Creating projectile motion dataset...")
    # Parameters
    v0 = 50  # Initial velocity (m/s)
    g = 9.81  # Gravity (m/s²)
    k = 0.01  # Air resistance coefficient
    # Launch angles (degrees)
    angles_deg = np.linspace(15, 75, 100)
    angles_rad = np.deg2rad(angles_deg)
    # Calculate range with air resistance (simplified model)
    # R ≈ (v₀²/g) * sin(2θ) * (1 - k*v₀*sin(θ))
    ranges = (v0**2 / g) * np.sin(2 * angles_rad) * (1 - k * v0 * np.sin(angles_rad))
    # Add realistic measurement noise
    noise = np.random.normal(0, 2, len(ranges))
    ranges_noisy = ranges + noise
    return angles_deg.reshape(-1, 1), ranges_noisy, ranges
def demonstrate_basic_regression():
    """Demonstrate basic linear regression workflow."""
    print("\n🚀 Basic Linear Regression Example")
    print("=" * 50)
    # 1. Generate dataset
    X, y_noisy, y_true = create_physics_dataset()
    print(f"Dataset created: {len(X)} data points")
    print(f"Feature: Launch angle (degrees)")
    print(f"Target: Projectile range (meters)")
    # 2. Split data
    split_idx = int(0.8 * len(X))
    X_train, X_test = X[:split_idx], X[split_idx:]
    y_train, y_test = y_noisy[:split_idx], y_noisy[split_idx:]
    print(f"\nData split: {len(X_train)} training, {len(X_test)} testing samples")
    # 3. Create and train model
    print("\n🔧 Training linear regression model...")
    model = LinearRegression(
        fit_intercept=True,
        solver='svd',  # Most stable solver
        uncertainty_estimation=True
    )
    model.fit(X_train, y_train)
    print("✅ Model training complete!")
    # 4. Make predictions
    y_pred = model.predict(X_test)
    y_pred_with_uncertainty = model.predict(X_test, return_uncertainty=True)
    if len(y_pred_with_uncertainty) == 2:
        y_pred, uncertainties = y_pred_with_uncertainty
        print(f"📈 Predictions generated with uncertainty estimates")
    else:
        y_pred = y_pred_with_uncertainty
        uncertainties = None
        print(f"📈 Predictions generated")
    # 5. Evaluate model
    evaluator = ModelEvaluator()
    results = evaluator.evaluate_regression(model, X_test, y_test)
    print(f"\n📊 Model Performance:")
    print(f"  R² Score: {results.r2:.4f}")
    print(f"  RMSE: {results.rmse:.2f} meters")
    print(f"  MAE: {results.mae:.2f} meters")
    # 6. Display model parameters
    summary = model.summary()
    print(f"\n🔍 Model Parameters:")
    print(f"  Intercept: {summary['intercept']:.4f}")
    print(f"  Coefficient: {summary['coefficients'][0]:.4f}")
    if 'coefficient_std_errors' in summary:
        print(f"  Coefficient Std Error: {summary['coefficient_std_errors'][0]:.4f}")
    # 7. Visualize results
    print(f"\n📈 Creating visualizations...")
    visualize_results(X, y_noisy, y_true, X_train, y_train, X_test, y_test,
                     y_pred, uncertainties, model)
    return model, results
def visualize_results(X, y_noisy, y_true, X_train, y_train, X_test, y_test,
                     y_pred, uncertainties, model):
    """Create comprehensive visualizations."""
    # Create figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    # Plot 1: Data and model fit
    ax1 = axes[0, 0]
    # Plot true function
    ax1.plot(X, y_true, '--', color='gray', linewidth=2, alpha=0.7, label='True Function')
    # Plot noisy data
    ax1.scatter(X_train, y_train, color=berkeley_blue, alpha=0.6, s=30, label='Training Data')
    ax1.scatter(X_test, y_test, color=california_gold, alpha=0.8, s=40,
               marker='s', label='Test Data')
    # Plot model predictions
    X_plot = np.linspace(X.min(), X.max(), 200).reshape(-1, 1)
    y_plot = model.predict(X_plot)
    ax1.plot(X_plot, y_plot, color='red', linewidth=2, label='Model Prediction')
    # Add uncertainty bands if available
    if uncertainties is not None:
        y_plot_with_unc = model.predict(X_plot, return_uncertainty=True)
        if len(y_plot_with_unc) == 2:
            y_plot, unc_plot = y_plot_with_unc
            ax1.fill_between(X_plot.ravel(), y_plot - 2*unc_plot, y_plot + 2*unc_plot,
                           alpha=0.2, color='red', label='95% Confidence')
    ax1.set_xlabel('Launch Angle (degrees)')
    ax1.set_ylabel('Range (meters)')
    ax1.set_title('Projectile Motion: Model Fit')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    # Plot 2: Predictions vs Actual
    ax2 = axes[0, 1]
    ax2.scatter(y_test, y_pred, color=berkeley_blue, alpha=0.7, s=50)
    # Perfect prediction line
    min_val, max_val = min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())
    ax2.plot([min_val, max_val], [min_val, max_val], '--', color=california_gold,
            linewidth=2, label='Perfect Prediction')
    ax2.set_xlabel('Actual Range (meters)')
    ax2.set_ylabel('Predicted Range (meters)')
    ax2.set_title('Predictions vs Actual Values')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    # Plot 3: Residuals
    ax3 = axes[1, 0]
    residuals = y_test - y_pred
    ax3.scatter(y_pred, residuals, color=berkeley_blue, alpha=0.7, s=50)
    ax3.axhline(y=0, color=california_gold, linestyle='--', linewidth=2)
    ax3.set_xlabel('Predicted Range (meters)')
    ax3.set_ylabel('Residuals (meters)')
    ax3.set_title('Residual Analysis')
    ax3.grid(True, alpha=0.3)
    # Plot 4: Model interpretation
    ax4 = axes[1, 1]
    # Show effect of angle on range
    angles = np.linspace(15, 75, 100).reshape(-1, 1)
    ranges_pred = model.predict(angles)
    ax4.plot(angles, ranges_pred, color=berkeley_blue, linewidth=3, label='Model Prediction')
    ax4.set_xlabel('Launch Angle (degrees)')
    ax4.set_ylabel('Predicted Range (meters)')
    ax4.set_title('Model Interpretation: Angle vs Range')
    ax4.grid(True, alpha=0.3)
    # Find optimal angle
    optimal_idx = np.argmax(ranges_pred)
    optimal_angle = angles[optimal_idx, 0]
    optimal_range = ranges_pred[optimal_idx]
    ax4.plot(optimal_angle, optimal_range, 'ro', markersize=10,
            label=f'Optimal: {optimal_angle:.1f}° → {optimal_range:.1f}m')
    ax4.legend()
    plt.suptitle('Linear Regression Analysis: Projectile Motion',
                fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()
def physics_insights():
    """Provide physics insights from the model."""
    print("\n🔬 Physics Insights")
    print("=" * 30)
    print("In ideal projectile motion (no air resistance):")
    print("• Optimal launch angle is 45°")
    print("• Range ∝ sin(2θ)")
    print("• Maximum range = v₀²/g")
    print()
    print("With air resistance:")
    print("• Optimal angle is slightly less than 45°")
    print("• Range decreases due to drag")
    print("• Our model captures this linear approximation")
def interactive_exploration():
    """Interactive exploration of the model."""
    print("\n🎮 Interactive Exploration")
    print("=" * 35)
    # Create a simple interactive demo
    model, _ = demonstrate_basic_regression()
    print("Try different launch angles:")
    test_angles = [30, 37, 45, 52, 60]
    for angle in test_angles:
        predicted_range = model.predict([[angle]])[0]
        print(f"  {angle:2d}° → {predicted_range:6.2f} meters")
    print("\nTry your own angles! (modify the test_angles list above)")
def main():
    """Main function to run the complete example."""
    print("🎯 Berkeley SciComp: Basic Linear Regression")
    print("=" * 55)
    print("Welcome to your first machine learning example!")
    print("We'll analyze projectile motion using linear regression.\n")
    try:
        # Run the main demonstration
        model, results = demonstrate_basic_regression()
        # Provide physics insights
        physics_insights()
        # Interactive exploration
        interactive_exploration()
        print("\n✨ Example completed successfully!")
        print("\nKey Takeaways:")
        print("• Linear regression finds the best linear relationship")
        print("• R² measures how well the model explains the data")
        print("• Residual analysis helps identify model limitations")
        print("• Uncertainty quantification provides confidence estimates")
        print("\nNext Steps:")
        print("• Try the polynomial regression example")
        print("• Explore non-linear relationships")
        print("• Learn about regularization techniques")
    except Exception as e:
        print(f"❌ Error occurred: {e}")
        print("Please check your installation and try again.")
if __name__ == "__main__":
    # Set random seed for reproducibility
    np.random.seed(42)
    # Run the example
    main()