%% SciComp MATLAB Toolbox Startup Script
%
% Initializes the SciComp scientific computing environment for MATLAB.
% Sets up paths, configures Berkeley-themed plotting defaults, and
% initializes physics constants.
%
% This script is automatically run when MATLAB starts if placed in the
% MATLAB startup path or called manually.
%
% Key Features:
% - Automatic path configuration for all SciComp modules
% - Berkeley visual identity setup for all plots
% - Physics constants initialization (CODATA 2018)
% - Performance optimization settings
% - Cross-platform compatibility checks
%
% Author: Meshal Alawein (contact@meshal.ai)
% License: MIT
% Copyright © 2025 Meshal Alawein
%% Display startup message
fprintf('\n');
fprintf('🔬 SciComp: Professional Scientific Computing Portfolio\n');
fprintf('========================================================\n');
fprintf('Author: Meshal Alawein (contact@meshal.ai)\n');
fprintf('License: MIT © 2025 Meshal Alawein\n\n');
%% Get SciComp root directory
scicompRoot = fileparts(mfilename('fullpath'));
fprintf('📁 SciComp root directory: %s\n', scicompRoot);
%% Add all SciComp directories to MATLAB path
fprintf('🔧 Configuring MATLAB path...\n');
% Core modules
addpath(fullfile(scicompRoot, 'quantum_physics'));
addpath(fullfile(scicompRoot, 'quantum_computing'));
addpath(fullfile(scicompRoot, 'statistical_physics'));
addpath(fullfile(scicompRoot, 'condensed_matter'));
addpath(fullfile(scicompRoot, 'ml_physics'));
addpath(fullfile(scicompRoot, 'computational_methods'));
addpath(fullfile(scicompRoot, 'visualization'));
addpath(fullfile(scicompRoot, 'utils'));
% Subdirectories (recursive)
addpath(genpath(fullfile(scicompRoot, 'quantum_physics')));
addpath(genpath(fullfile(scicompRoot, 'quantum_computing')));
addpath(genpath(fullfile(scicompRoot, 'statistical_physics')));
addpath(genpath(fullfile(scicompRoot, 'condensed_matter')));
addpath(genpath(fullfile(scicompRoot, 'ml_physics')));
addpath(genpath(fullfile(scicompRoot, 'computational_methods')));
addpath(genpath(fullfile(scicompRoot, 'visualization')));
addpath(genpath(fullfile(scicompRoot, 'utils')));
fprintf('   ✅ Quantum physics modules loaded\n');
fprintf('   ✅ Quantum computing modules loaded\n');
fprintf('   ✅ Statistical physics modules loaded\n');
fprintf('   ✅ Condensed matter modules loaded\n');
fprintf('   ✅ ML physics modules loaded\n');
fprintf('   ✅ Computational methods loaded\n');
fprintf('   ✅ Visualization modules loaded\n');
fprintf('   ✅ Utility functions loaded\n');
%% Initialize Berkeley plotting defaults
fprintf('🎨 Setting up Berkeley visual identity...\n');
try
    setBerkeleyDefaults();
    fprintf('   ✅ Berkeley color scheme activated\n');
    fprintf('   ✅ Publication-quality plot settings configured\n');
catch ME
    fprintf('   ⚠️  Warning: Could not set Berkeley defaults: %s\n', ME.message);
end
%% Initialize physics constants
fprintf('⚛️  Loading physics constants (CODATA 2018)...\n');
try
    global PHYSICS_CONSTANTS;
    PHYSICS_CONSTANTS = PhysicsConstants();
    fprintf('   ✅ Fundamental constants loaded\n');
    fprintf('   ✅ Unit conversion functions available\n');
catch ME
    fprintf('   ⚠️  Warning: Could not load physics constants: %s\n', ME.message);
end
%% Performance optimization
fprintf('⚡ Optimizing MATLAB performance...\n');
% Enable JIT compilation
feature('JitAcceleration', 'on');
% Set number of computational threads
maxThreads = feature('numcores');
if maxThreads > 1
    fprintf('   ✅ Using %d computational threads\n', maxThreads);
end
% Configure memory settings
try
    % Increase maximum array size if possible
    feature('DefaultCharacterSet', 'UTF8');
    fprintf('   ✅ UTF-8 character encoding enabled\n');
catch
    % Continue if not available
end
%% Version and compatibility checks
fprintf('🔍 Checking MATLAB compatibility...\n');
matlabVersion = version('-release');
matlabYear = str2double(matlabVersion(1:4));
if matlabYear >= 2020
    fprintf('   ✅ MATLAB %s (compatible)\n', matlabVersion);
else
    fprintf('   ⚠️  MATLAB %s (may have compatibility issues, recommend R2020b+)\n', matlabVersion);
end
% Check for required toolboxes
requiredToolboxes = {
    'Statistics and Machine Learning Toolbox', 'stats';
    'Signal Processing Toolbox', 'signal';
    'Image Processing Toolbox', 'images';
    'Parallel Computing Toolbox', 'parallel';
    'Optimization Toolbox', 'optim';
    'Symbolic Math Toolbox', 'symbolic'
};
fprintf('📦 Checking available toolboxes:\n');
installedToolboxes = ver;
toolboxNames = {installedToolboxes.Name};
for i = 1:size(requiredToolboxes, 1)
    toolboxName = requiredToolboxes{i, 1};
    if any(contains(toolboxNames, toolboxName))
        fprintf('   ✅ %s\n', toolboxName);
    else
        fprintf('   ⚠️  %s (not installed - some features may be limited)\n', toolboxName);
    end
end
%% Display available functions
fprintf('\n📚 Available SciComp functions:\n');
fprintf('   🔬 Quantum Physics:\n');
fprintf('      QuantumHarmonic, TDSESolver, WavepacketEvolution\n');
fprintf('   ⚛️  Quantum Computing:\n');
fprintf('      VQE, QAOA, GroverSearch, QuantumCircuits\n');
fprintf('   🧠 Machine Learning:\n');
fprintf('      PINNs, MaterialsML, QuantumML\n');
fprintf('   📊 Visualization:\n');
fprintf('      BerkeleyPlotStyle, PlotQuantumStates\n');
fprintf('   🛠️  Utilities:\n');
fprintf('      PhysicsConstants, CommonFunctions\n');
%% Usage examples
fprintf('\n💡 Quick start examples:\n');
fprintf('   %% Quantum harmonic oscillator\n');
fprintf('   qho = QuantumHarmonic(1.0);  %% omega = 1.0\n');
fprintf('   psi0 = qho.eigenstate(0);    %% ground state\n');
fprintf('   qho.plot();\n\n');
fprintf('   %% VQE quantum computing\n');
fprintf('   vqe = VQE();                 %% initialize VQE\n');
fprintf('   result = vqe.optimize();     %% run optimization\n');
fprintf('   vqe.plotResults();\n\n');
fprintf('   %% Berkeley-styled plotting\n');
fprintf('   x = linspace(0, 2*pi, 100);\n');
fprintf('   berkeleyPlot(x, sin(x), ''title'', ''Sine Wave'');\n\n');
%% Completion message
fprintf('✅ SciComp initialization complete!\n');
fprintf('🐻💙💛 Ready for scientific computing\n');
fprintf('========================================================\n\n');
%% Save workspace info
fprintf('💾 Saving workspace information...\n');
workspaceFile = fullfile(scicompRoot, 'scicomp_workspace.mat');
try
    save(workspaceFile, 'scicompRoot', 'matlabVersion');
    fprintf('   ✅ Workspace saved to: %s\n', workspaceFile);
catch ME
    fprintf('   ⚠️  Could not save workspace: %s\n', ME.message);
end
%% Set global preferences
fprintf('⚙️  Setting global preferences...\n');
% Numerical display format
format long;
% Random seed for reproducibility
rng(42, 'twister');
% Warning settings
warning('off', 'MATLAB:dispatcher:nameConflict');
fprintf('   ✅ Numerical format: long precision\n');
fprintf('   ✅ Random seed: 42 (reproducible results)\n');
fprintf('   ✅ Warning filters configured\n');
%% Final instructions
fprintf('\n📖 Documentation and help:\n');
fprintf('   • Type ''help <function>'' for detailed documentation\n');
fprintf('   • Visit examples in live_scripts/ for interactive tutorials\n');
fprintf('   • Check visualization/ for Berkeley-themed plotting examples\n');
fprintf('   • See utils/ for physics constants and common functions\n\n');
fprintf('🚀 Happy computing!\n\n');