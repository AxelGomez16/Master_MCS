import numpy as np
import plotly.graph_objects as go

# data = np.array([30, 35, 33, 36, 34, 32, 35, 33, 34, 31, 36, 35]) # FONDO RAIZ
# data = np.array([45, 55, 50, 48, 52, 51, 53, 49, 50, 50, 49, 51]) # Patrimonio cuspide
data = np.array([100, 10, 80, 20, 120, - 20, 90, 10, 70, 30, 110, -10]) # Quantum



mean = np.mean(data)
median = np.median(data)
var_pop = np.var(data)
std_pop = np.std(data)


print("Media:", mean)
print("Mediana:", median)
print("Varianza:", var_pop)
print("Desviacion Estandar:", std_pop)


fig = go.Figure()

fig.add_trace(go.Scatter(
    x=list(range(1, len(data)+1)),
    y=data,
    mode="markers+lines",
    name="Data",
    marker=dict(size=10, color="blue")
))

fig.add_hline(y=mean, line=dict(color="red", dash="dash"), annotation_text=f"Media = {mean:.2f}")

fig.add_hline(y=median, line=dict(color="green", dash="dot"), annotation_text=f"Mediana = {median:.2f}")

fig.add_hline(y=mean+std_pop, line=dict(color="orange", dash="dash"), annotation_text=f"+1σ = {mean+std_pop:.2f}")
fig.add_hline(y=mean-std_pop, line=dict(color="orange", dash="dash"), annotation_text=f"-1σ = {mean-std_pop:.2f}")


# fig.add_hline(y=mean+var_pop, line=dict(color="pink", dash="dash"), annotation_text=f"+1σ = {mean-var_pop:.2f}")
# fig.add_hline(y=mean-var_pop, line=dict(color="pink", dash="dash"), annotation_text=f"-1σ = {mean-var_pop:.2f}")
#


fig.update_layout(
    title="Fondo Raiz - Data",
    xaxis_title="Datos",
    yaxis_title="Valores",
    template="plotly_white"
)

fig.show()
