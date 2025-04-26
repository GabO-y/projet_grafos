import heapq
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.colors as mcolors

# Definindo o grafo com as cidades e conexões fornecidas
graph = {
    'Açu': {'Angicos': 41.4, 'Mossoró': 69.4, 'Paraú': 36.7, 'Jucurutu': 78.9, 
            'Alfonso_Bezera': 62.5, 'Canaubais': 29.9, 'Campo_Grande': 62.5},
    'Angicos': {'Açu': 41.4, 'Lajes': 45.0, 'Currais_Novos': 112.0, 
                'Alfonso_Bezera': 23.2, 'Canaubais': 72.9},
    'Apodi': {'Mossoró': 82.0, 'Felipe_de_Guerra': 22.8, 'Caraúbas': 49.6},
    'Caiçara_do_Rio_do_Vento': {'Lajes': 28.1, 'Santa_Maria': 38.2, 
                                'Currais_Novos': 113.0, 'Joao_Camara': 43.7},
    'Lajes': {'Angicos': 45.0, 'Caiçara_do_Rio_do_Vento': 28.1, 'Santa_Cruz': 91.5,
              'Currais_Novos': 92.1, 'Jucurutu': 115.0, 'Joao_Camara': 65.3, 
              'Alfonso_Bezera': 44.0},
    'Macaíba': {'Natal': 27.7, 'Parnamirin': 16.2, 'Santa_Maria': 39.5,
                'Sao_Paulo_do_Potangi': 51.7, 'Santa_Cruz': 95.6, 'Ceará_mirim': 72.9},
    'Mossoró': {'Açu': 69.4, 'Apodi': 82.0, 'Felipe_de_Guerra': 72.8,
                'Canaubais': 72.9, 'Campo_Grande': 83.7},
    'Natal': {'Macaíba': 27.7, 'Parnamirin': 20.3, 'Ceará_mirim': 33.6},
    'Parnamirin': {'Macaíba': 16.2, 'Natal': 20.3, 'Santa_Cruz': 116.0},
    'Santa_Maria': {'Caiçara_do_Rio_do_Vento': 38.2, 'Macaíba': 39.5,
                    'Sao_Paulo_do_Potangi': 15.9},
    'Sao_Paulo_do_Potangi': {'Macaíba': 51.7, 'Santa_Maria': 15.9, 'Santa_Cruz': 72.1},
    'Felipe_de_Guerra': {'Apodi': 22.8, 'Mossoró': 72.8, 'Caraúbas': 35.9},
    'Paraú': {'Açu': 36.7, 'Caraúbas': 60.4},
    'Caraúbas': {'Apodi': 49.6, 'Felipe_de_Guerra': 35.9, 'Paraú': 60.4, 
                 'Campo_Grande': 31.7},
    'Santa_Cruz': {'Lajes': 91.5, 'Macaíba': 95.6, 'Parnamirin': 116.0,
                   'Sao_Paulo_do_Potangi': 72.1, 'Currais_Novos': 65.0,
                   'Ceará_mirim': 39.2, 'Joao_Camara': 50.5},
    'Currais_Novos': {'Angicos': 112.0, 'Caiçara_do_Rio_do_Vento': 113.0,
                      'Lajes': 92.1, 'Santa_Cruz': 65.0, 'Jucurutu': 70.1},
    'Jucurutu': {'Açu': 78.9, 'Lajes': 115.0, 'Currais_Novos': 70.1,
                 'Campo_Grande': 46.6},
    'Ceará_mirim': {'Natal': 33.6, 'Macaíba': 72.9, 'Santa_Cruz': 39.2,
                    'Joao_Camara': 47.7},
    'Joao_Camara': {'Caiçara_do_Rio_do_Vento': 43.7, 'Lajes': 65.3,
                    'Santa_Cruz': 50.5, 'Ceará_mirim': 47.7, 'Alfonso_Bezera': 91.9},
    'Alfonso_Bezera': {'Açu': 62.5, 'Angicos': 23.2, 'Lajes': 44.0,
                       'Canaubais': 55.2, 'Joao_Camara': 91.9},
    'Canaubais': {'Açu': 29.9, 'Angicos': 72.9, 'Mossoró': 72.9, 'Alfonso_Bezera': 55.2},
    'Campo_Grande': {'Açu': 62.5, 'Mossoró': 83.7, 'Caraúbas': 31.7, 'Jucurutu': 46.6}
}

# Implementação do algoritmo de Dijkstra com animação
def dijkstra_animation(graph, start, end):
    # Inicialização
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    previous_nodes = {node: None for node in graph}
    priority_queue = [(0, start)]
    
    # Criar grafo para visualização
    G = nx.Graph()
    for node in graph:
        G.add_node(node)
        for neighbor, weight in graph[node].items():
            G.add_edge(node, neighbor, weight=weight)
    
    # Posicionamento dos nós
    pos = nx.spring_layout(G, seed=42)
    
    # Configuração da figura
    fig, ax = plt.subplots(figsize=(12, 10))
    plt.title(f"Algoritmo de Dijkstra: {start} → {end}", fontsize=14)
    
    # Variáveis para armazenar o estado da animação
    visited_nodes = []
    current_node = None
    current_edges = []
    path_edges = []
    
    def update(frame):
        nonlocal priority_queue, distances, previous_nodes, visited_nodes, current_node, current_edges, path_edges
        
        ax.clear()
        
        if frame == 0:
            # Estado inicial
            nx.draw_networkx_nodes(G, pos, node_color='lightblue', ax=ax)
            nx.draw_networkx_labels(G, pos, ax=ax)
            nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.5, ax=ax)
            ax.set_title(f"Estado Inicial - Próximo: {start}", fontsize=12)
            return
        
        if not priority_queue:
            # Reconstruir caminho final
            if path_edges:
                node = end
                path = []
                while node is not None:
                    path.append(node)
                    node = previous_nodes[node]
                path.reverse()
                
                path_edges = list(zip(path[:-1], path[1:]))
                
                nx.draw_networkx_nodes(G, pos, node_color='lightblue', ax=ax)
                nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', ax=ax)
                nx.draw_networkx_labels(G, pos, ax=ax)
                nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3, ax=ax)
                nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax)
                
                total_distance = distances[end]
                ax.set_title(f"Caminho encontrado: {' → '.join(path)}\nDistância total: {total_distance} km", fontsize=12)
            return
        
        # Extrair o nó com menor distância
        current_distance, current_node = heapq.heappop(priority_queue)
        
        # Se já encontramos um caminho melhor, ignorar
        if current_distance > distances[current_node]:
            return
        
        visited_nodes.append(current_node)
        
        # Atualizar distâncias para vizinhos
        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight
            
            # Se encontrarmos um caminho melhor
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))
                current_edges.append((current_node, neighbor))
        
        # Desenhar o grafo
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', ax=ax)
        nx.draw_networkx_nodes(G, pos, nodelist=visited_nodes, node_color='green', ax=ax)
        if current_node:
            nx.draw_networkx_nodes(G, pos, nodelist=[current_node], node_color='yellow', ax=ax)
        nx.draw_networkx_labels(G, pos, ax=ax)
        
        # Desenhar todas as arestas
        nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.3, ax=ax)
        
        # Destacar arestas atuais sendo avaliadas
        if current_edges:
            nx.draw_networkx_edges(G, pos, edgelist=current_edges[-len(graph[current_node]):], 
                                 edge_color='orange', width=2, ax=ax)
        
        # Se encontramos o destino, começar a reconstruir o caminho
        if current_node == end:
            node = end
            path = []
            while node is not None:
                path.append(node)
                node = previous_nodes[node]
            path.reverse()
            path_edges = list(zip(path[:-1], path[1:]))
        
        # Desenhar o caminho encontrado até agora
        if path_edges:
            nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='red', width=2, ax=ax)
            nx.draw_networkx_nodes(G, pos, nodelist=path, node_color='red', ax=ax)
        
        # Atualizar título
        ax.set_title(f"Visitando: {current_node}\nDistância atual: {current_distance} km", fontsize=12)
        
        # Resetar arestas atuais para o próximo frame
        if frame % 2 == 0:
            current_edges = []
    
    # Criar animação
    frames = len(graph) * 3 + 2  # Número suficiente de frames
    ani = FuncAnimation(fig, update, frames=frames, interval=800, repeat=False)
    plt.tight_layout()
    plt.show()
    
    # Retornar o caminho final e distância
    node = end
    path = []
    while node is not None:
        path.append(node)
        node = previous_nodes[node]
    path.reverse()
    
    return path, distances[end]

# Executar o algoritmo com animação
start_city = 'Apodi'
end_city = 'Natal'
shortest_path, total_distance = dijkstra_animation(graph, start_city, end_city)

print(f"\nCaminho mais curto de {start_city} para {end_city}:")
print(" → ".join(shortest_path))
print(f"Distância total: {total_distance} km")