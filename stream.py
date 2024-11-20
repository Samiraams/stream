import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# Título e Introdução
st.title("Compressão e Descompressão de arquivos com LZW")
st.markdown("""
            
Este relatório apresenta os resultados e análises do Trabalho Prático, realizado para a disciplina **DCC207 - Algoritmos 2**. 
O objetivo foi implementar o algoritmo de compressão LZW em duas implementações distintas e avaliar seu desempenho com diferentes tipos de dados.
                     
### Integrantes:

- Samira Malaquias       2022107580
- Victoria Estanislau    2021037490
            
---
            
""")



# Explicação do Algoritmo
st.header("Explicação do Algoritmo LZW e Métodos Utilizados")
st.markdown("""
O algoritmo **LZW (Lempel-Ziv-Welch)** é uma técnica de compressão sem perdas que substitui padrões repetidos nos dados por códigos inteiros, usando um **dicionário dinâmico** para mapear sequências de entrada. A seguir, explicamos as implementações da compressão e descompressão estática e dinâmica, com suporte para dicionários de tamanhos variáveis.          

### 1. Codificação Estática (`lzw_encoder`)
Na codificação estática, o código do dicionário tem um tamanho fixo, determinado pelo parâmetro `bits_max`, que define o número máximo de bits para representar os códigos. O processo é descrito a seguir:          
            
- **Inicialização do Dicionário**:
  - O dicionário começa com todas as sequências de um único byte (256 entradas), mapeadas para seus códigos ASCII correspondentes.
- **Construção do Dicionário**:
  - À medida que os dados são lidos, o algoritmo verifica se uma sequência já existe no dicionário:
    - Se a sequência existe, ela é ampliada com o próximo byte.
    - Caso contrário, a sequência anterior é codificada, adicionada ao dicionário com um novo código, e a sequência atual é redefinida.
- **Codificação Final**:
  - No final da entrada, quaisquer sequências restantes também são codificadas e adicionadas ao dicionário.

Essa abordagem mantém o tamanho do dicionário estável, mas é limitada por `bits_max`.

### 2. Decodificação Estática (`lzw_decoder`)
Na decodificação estática, o processo reverte a codificação para reconstruir os dados originais. Ele utiliza um dicionário que:
- Inicializa com as 256 sequências de um byte.
- Reconstrói sequências conforme os códigos são lidos, adicionando novas combinações ao dicionário.

A decodificação também verifica se o código lido é válido, gerando erros para códigos inválidos.

### 3. Codificação Dinâmica (`lzw_encoder_variable`)
A versão dinâmica permite o crescimento do dicionário com um número variável de bits, começando em 9 bits e aumentando progressivamente até o limite `bits_max`. O processo inclui:

- **Ajuste do Tamanho do Dicionário**:
  - Sempre que o número de códigos no dicionário ultrapassa o limite de bits atual, o número de bits utilizados é incrementado.
  - O limite do dicionário cresce de forma exponencial com cada incremento nos bits.
- **Eficiência Dinâmica**:
  - Essa abordagem melhora a compressão para arquivos grandes, onde padrões adicionais são identificados e representados com mais precisão.

### 4. Decodificação Dinâmica (`lzw_decoder_variable`)
A decodificação dinâmica reconstrói os dados compactados, adaptando-se ao tamanho variável do dicionário:

- **Incremento dos Bits**:
  - Sempre que o número de códigos no dicionário ultrapassa o limite de bits atual, o decodificador aumenta a largura dos códigos.
- **Reconstrução Dinâmica**:
  - O decodificador recria sequências conforme os códigos são lidos, garantindo que novos padrões sejam adicionados ao dicionário à medida que aparecem.

### 5. Manipulação de Bits
Para lidar com tamanhos variáveis de códigos na versão dinâmica do LZW, são utilizados os utilitários `Bit_writer` e `Bit_reader`, que permitem a leitura e escrita de números inteiros com um número específico de bits.

- **Bit_writer**: 
  - Compacta os códigos em sequência, garantindo alinhamento adequado ao salvar no arquivo.
- **Bit_reader**:
  - Lê os códigos compactados do arquivo e os reconstrói para serem interpretados pelo algoritmo.

### Benefícios e Limitações
- A compressão estática é simples e eficiente para entradas menores ou padrões previsíveis.
- A compressão dinâmica é ideal para entradas maiores, oferecendo melhor compactação ao adaptar o tamanho do dicionário.
- Manipular tamanhos de bits requer maior controle de memória e precisão para evitar erros de alinhamento.

""")

# Análises e Resultados
st.image("images/compression_rate_vs_bits", caption="", use_column_width=True)
st.image("images/compression_rate_vs_time_fixed", caption="", use_column_width=True)
st.image("images/compression_rate_vs_time_variable", caption="", use_column_width=True)
st.image("images/dictionary_growth_fixed.png", caption="", use_column_width=True)
st.image("images/dictionary_growth_variable.png", caption="", use_column_width=True)
st.image("images/execution_time_vs_bits.png", caption="", use_column_width=True)
st.image("images/heatmap_compression_rate.png", caption="", use_column_width=True)

# Conclusão
st.header("Conclusão")
st.markdown("""
O algoritmo LZW provou ser altamente eficiente e versátil em diferentes cenários de compressão, apresentando resultados que variam conforme o tipo de arquivo e a configuração do dicionário. Nos testes realizados, foram avaliados arquivos de texto com tamanho de 74.248 bits e arquivos de imagem bitmap com 2.097.584 bits, considerando versões dinâmica e estática do algoritmo, e o impacto de diferentes números máximos de bits variando entre 9 e 16.

Para arquivos de texto, o LZW atingiu taxas de compressão elevadas, com um máximo de 47,81%, demonstrando alta eficiência em identificar e compactar padrões repetitivos típicos desse formato. Além disso, o tempo de compressão e descompressão foi insignificante, permanecendo estável independentemente do tamanho do dicionário, o que reflete a simplicidade dos padrões encontrados nos textos.

Por outro lado, em arquivos de imagem bitmap, as taxas de compressão foram mais variáveis, alcançando até 59,5% com dicionários maiores. O tempo de compressão e descompressão foi significativamente mais elevado em comparação aos textos, especialmente para configurações com dicionários pequenos. No entanto, observou-se uma redução substancial nos tempos à medida que o número máximo de bits aumentava, indicando que dicionários maiores conseguem otimizar de forma expressiva o desempenho para arquivos de imagem, que possuem padrões mais complexos.

Em suma, o LZW é uma ferramenta poderosa para compressão de dados, mas seu desempenho depende diretamente das características do arquivo e da configuração do dicionário. Futuros trabalhos podem explorar variantes do LZW, como versões adaptativas, para lidar com diferentes tipos de dados e aumentar a eficiência em cenários mais diversos. Além disso, incluir testes com outros formatos de arquivo, como áudio e vídeo, pode expandir ainda mais a aplicabilidade do algoritmo.
""")
