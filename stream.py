import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# Título e introdução
st.title("Relatório do Trabalho Prático - Algoritmo LZW")
st.markdown("""
Este relatório apresenta os resultados e análises do trabalho prático para a disciplina **DCC207 - Algoritmos 2**. 
O objetivo foi implementar o algoritmo de compressão LZW e avaliar seu desempenho com diferentes tipos de dados.
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
Para lidar com tamanhos variáveis de códigos, são utilizados os utilitários `Bit_writer` e `Bit_reader`, que permitem a leitura e escrita de números inteiros com um número específico de bits.

- **Bit_writer**: 
  - Compacta os códigos em sequência, garantindo alinhamento adequado ao salvar no arquivo.
- **Bit_reader**:
  - Lê os códigos compactados do arquivo e os reconstrói para serem interpretados pelo algoritmo.

### Benefícios e Limitações
- A compressão estática é simples e eficiente para entradas menores ou padrões previsíveis.
- A compressão dinâmica é ideal para entradas maiores, oferecendo melhor compactação ao adaptar o tamanho do dicionário.
- Manipular tamanhos de bits requer maior controle de memória e precisão para evitar erros de alinhamento.

""")

# Análise de Resultados
st.header("Análise de Resultados")

# Dados para .txt
bits_txt = [ 9, 10, 11, 12, 13, 14, 15, 16]
taxas_txt = [ 30.9, 43.21, 46.36, 47.81, 47.81, 47.81, 47.81, 47.81]
tempos_compressao_txt = [ 0.0180, 0.0149, 0.0149, 0.0164, 0.0165, 0.0166, 0.0164, 0.0165]
tempos_descompressao_txt = [ 0.0138, 0.0094, 0.0082, 0.0077, 0.0077, 0.0076, 0.0077, 0.0076]
dicionarios_txt = [ 512, 1024, 2048, 3719, 3719, 3719, 3719, 3719]





# Dados para .bmp
bits_bmp = [9, 10, 11, 12, 13, 14, 15, 16]
taxas_bmp = [15.40, 16.04, 12.69, 17.34, 23.04, 36.50, 42.11, 59.50]
tempos_compressao_bmp = [8.9485, 8.4329, 8.7302, 7.7132, 6.2825, 4.3491, 3.6656, 1.8558]
tempos_descompressao_bmp = [7.4777, 6.9839, 7.0999, 6.0964, 5.2198, 3.4313, 2.7524, 1.3343]
dicionarios_bmp = [512, 1024, 2048, 4096, 8192, 16384, 32768, 57304]


st.markdown("""
Todas as análises apresentadas neste relatório foram realizadas considerando arquivos de imagem .bmp com tamanho de 2.097.584 bits e arquivos de texto .txt com tamanho de 74.248 bits. As avaliações abrangem tanto a versão estática quanto a dinâmica do algoritmo LZW, levando em conta diferentes configurações para o número máximo de bits no dicionário, variando de 9 a 16. Esse enfoque permite uma compreensão detalhada do desempenho do algoritmo em relação a diferentes tipos de dados e tamanhos de dicionário, considerando aspectos como tempo de compressão, tempo de descompressão, crescimento do dicionário e taxa de compressão.
""")








# Taxa de Compressão: Comparação entre .txt e .bmp
st.header("Comparação: Taxa de Compressão vs. Número Máximo de Bits")
fig1, ax1 = plt.subplots()
ax1.plot(bits_txt, taxas_txt, label="Arquivo .txt", marker="o")
ax1.plot(bits_bmp, taxas_bmp, label="Arquivo .bmp", marker="s")
ax1.set_xlabel("Número Máximo de Bits")
ax1.set_ylabel("Taxa de Compressão (%)")
ax1.set_title("Taxa de Compressão em Relação ao Número Máximo de Bits")
ax1.legend()
ax1.grid()
st.pyplot(fig1)


st.markdown("""
O gráfico "Taxa de Compressão em Relação ao Número Máximo de Bits" compara o desempenho do algoritmo LZW em arquivos .txt e .bmp, mostrando como a taxa de compressão varia com o aumento do número máximo de bits utilizado no dicionário. Ele revela comportamentos distintos entre os dois tipos de arquivos, refletindo as diferenças estruturais e de redundância inerentes a cada formato.

Para o arquivo .txt, observa-se que a taxa de compressão cresce rapidamente até 12 bits, atingindo cerca de 47,81%. A partir deste ponto, a taxa se estabiliza, independentemente do aumento no número máximo de bits. Esse comportamento indica que, para o arquivo .txt, o dicionário alcança uma capacidade ótima em 12 bits, onde padrões suficientes são representados, e o aumento do tamanho do dicionário não traz melhorias adicionais.

Por outro lado, o arquivo .bmp apresenta um comportamento diferente. A taxa de compressão começa relativamente baixa, em torno de 15,4% com 9 bits, e cresce lentamente até 13 bits. A partir de 14 bits, o crescimento se torna mais expressivo, alcançando taxas de 36,5% com 14 bits e 59,5% com 16 bits. Esse padrão reflete o fato de que arquivos .bmp, por serem formatos mais estruturados e com menos redundância textual, requerem dicionários maiores para identificar e aproveitar padrões significativos.

Comparando os dois tipos de arquivo, nota-se que o formato .txt se beneficia mais rapidamente de dicionários menores, enquanto o formato .bmp requer um maior número de bits para alcançar ganhos significativos na taxa de compressão. Isso demonstra que a eficiência do LZW depende não apenas do número máximo de bits, mas também das características do arquivo de entrada.
""")



# Tempo Total de Compressão e Descompressão
st.header("Comparação: Tempo de Compressão e Descompressão")
fig2, ax2 = plt.subplots()
ax2.plot(bits_txt, tempos_compressao_txt, label="Compressão .txt", marker="o")
ax2.plot(bits_txt, tempos_descompressao_txt, label="Descompressão .txt", marker="s")
ax2.plot(bits_bmp, tempos_compressao_bmp, label="Compressão .bmp", marker="^")
ax2.plot(bits_bmp, tempos_descompressao_bmp, label="Descompressão .bmp", marker="v")
ax2.set_xlabel("Número Máximo de Bits")
ax2.set_ylabel("Tempo (s)")
ax2.set_title("Tempo de Compressão e Descompressão")
ax2.legend()
ax2.grid()
st.pyplot(fig2)

st.markdown("""
O gráfico "Tempo de Compressão e Descompressão" apresenta a relação entre o número máximo de bits configurados no algoritmo LZW e o tempo total de compressão e descompressão para arquivos .txt e .bmp. Ele ilustra claramente o impacto do tamanho do dicionário no desempenho do algoritmo, tanto para compressão quanto para descompressão, com diferenças significativas entre os dois tipos de arquivo.

Para arquivos .txt, o tempo de compressão e descompressão é consistentemente baixo, com valores próximos de zero, independentemente do número máximo de bits. Esse comportamento reflete a menor complexidade de compressão em arquivos de texto, que geralmente possuem padrões mais simples e repetitivos, permitindo que o algoritmo opere de forma eficiente com dicionários menores.

Já para arquivos .bmp, o tempo de compressão é significativamente maior no início, especialmente para valores baixos de bits máximos (9 a 11). O tempo de compressão para esses casos começa próximo de 9 segundos e diminui gradualmente à medida que o número máximo de bits aumenta, atingindo cerca de 2 segundos em 16 bits. Esse padrão sugere que, com dicionários maiores, o algoritmo consegue representar padrões de forma mais eficiente, reduzindo o número de operações necessárias durante o processamento.

O tempo de descompressão para arquivos .bmp segue uma tendência similar, mas é ligeiramente menor que o tempo de compressão. No entanto, ambos os tempos diminuem de forma acentuada a partir de 13 bits, refletindo uma otimização no processo de decodificação quando o dicionário é suficientemente grande para conter as sequências do arquivo comprimido.

Comparando os dois tipos de arquivo, é evidente que a compressão e a descompressão de arquivos .bmp demandam significativamente mais tempo que arquivos .txt, devido à maior complexidade de padrões e à natureza mais estruturada dos dados em imagens. No entanto, o impacto do número máximo de bits no desempenho é mais pronunciado para .bmp, indicando que a escolha de um valor adequado de bits é crucial para otimizar o tempo de execução. As linhas que representam o tempo de compressão e descompressão para arquivos .txt estão praticamente sobreposta
""")



# Crescimento do Dicionário: Comparação entre .txt e .bmp
st.header("Comparação: Crescimento do Dicionário")
fig3, ax3 = plt.subplots()
ax3.plot(bits_txt, dicionarios_txt, label="Dicionário .txt", marker="o")
ax3.plot(bits_bmp, dicionarios_bmp, label="Dicionário .bmp", marker="s")
ax3.set_xlabel("Número Máximo de Bits")
ax3.set_ylabel("Tamanho do Dicionário (Entradas)")
ax3.set_title("Crescimento do Dicionário em Relação ao Número Máximo de Bits")
ax3.legend()
ax3.grid()
st.pyplot(fig3)

st.markdown("""
O gráfico "Crescimento do Dicionário em Relação ao Número Máximo de Bits" apresenta o impacto do número máximo de bits no tamanho do dicionário para os arquivos .txt e .bmp. Ele demonstra claramente diferenças no comportamento do algoritmo LZW para esses dois tipos de arquivos, refletindo a natureza dos padrões e redundâncias em seus dados.

Para o arquivo .txt, o tamanho do dicionário se estabiliza rapidamente em torno de 3719 entradas, independentemente do número máximo de bits permitido. Isso sugere que os padrões presentes no arquivo .txt são suficientemente capturados com um dicionário de tamanho modesto. O crescimento inicial é pequeno, e, a partir de 12 bits, não há expansão adicional do dicionário, indicando que o arquivo não contém complexidade suficiente para aproveitar dicionários maiores.

Por outro lado, o arquivo .bmp apresenta um comportamento completamente diferente. O tamanho do dicionário cresce exponencialmente à medida que o número máximo de bits aumenta, atingindo mais de 57.000 entradas com 16 bits. Esse crescimento reflete a maior complexidade estrutural e a menor redundância dos dados em arquivos de imagem. À medida que o dicionário é expandido, o algoritmo consegue identificar e armazenar padrões mais longos e complexos, resultando em um aumento significativo no número de entradas.

Comparando os dois tipos de arquivo, é evidente que os arquivos .bmp exigem dicionários muito maiores para alcançar eficiência na compressão. Enquanto os dados em arquivos .txt são mais regulares e redundantes, facilitando o uso de dicionários menores, os arquivos .bmp apresentam uma diversidade maior de padrões, que requerem mais entradas no dicionário para serem representados adequadamente.
""")


# 1. Scatter Plot: Taxa de Compressão x Tempo de Compressão
st.header("Análise: Taxa de Compressão x Tempo de Compressão")
fig1, ax1 = plt.subplots()
ax1.scatter(tempos_compressao_txt, taxas_txt, label="Arquivo .txt", color="blue")
ax1.scatter(tempos_compressao_bmp, taxas_bmp, label="Arquivo .bmp", color="green")
ax1.set_xlabel("Tempo de Compressão (s)")
ax1.set_ylabel("Taxa de Compressão (%)")
ax1.set_title("Taxa de Compressão x Tempo de Compressão")
ax1.legend()
ax1.grid()
st.pyplot(fig1)

st.markdown("""
O gráfico "Taxa de Compressão x Tempo de Compressão" mostra a relação entre a eficiência da compressão (em termos de taxa de compressão) e o tempo necessário para comprimir os arquivos .txt e .bmp. Ele evidencia diferenças significativas entre os dois tipos de arquivo, destacando como as características do conteúdo impactam o desempenho do algoritmo LZW.

Para arquivos .txt, observa-se que a compressão é extremamente rápida, com tempos próximos de zero, independentemente da taxa de compressão alcançada. Todas as taxas de compressão ficam acima de 40%, com várias configurações atingindo aproximadamente 47,81%. Esse comportamento reflete a simplicidade de padrões em arquivos de texto, que são rapidamente processados pelo algoritmo, mesmo com dicionários menores.

Já para arquivos .bmp, a relação entre a taxa de compressão e o tempo de compressão é bem mais dispersa. O tempo de compressão começa elevado (próximo de 9 segundos) para taxas de compressão relativamente baixas (cerca de 15% a 20%). No entanto, à medida que o tempo de compressão diminui, observa-se um aumento considerável na taxa de compressão, chegando a 59,5% com tempos em torno de 2 segundos. Esse padrão sugere que dicionários maiores, configurados para valores mais altos de bits máximos, não apenas melhoram a eficiência da compressão, mas também reduzem o tempo necessário para processar o arquivo.

Comparando os dois tipos de arquivo, é evidente que o algoritmo LZW comprime arquivos .txt com alta eficiência e em tempos insignificantes, devido à maior redundância nos dados. Por outro lado, arquivos .bmp apresentam um compromisso mais claro entre tempo e eficiência: taxas de compressão mais altas exigem configurações específicas que otimizam o uso de padrões complexos no dicionário.
""")


# Criando o DataFrame para Heatmaps
tempo_data = pd.DataFrame({
    "Número de Bits": bits_txt + bits_bmp,
    "Tempo Compressão (s)": tempos_compressao_txt + tempos_compressao_bmp,
    "Tempo Descompressão (s)": tempos_descompressao_txt + tempos_descompressao_bmp,
    "Tipo de Arquivo": ["txt"] * len(bits_txt) + ["bmp"] * len(bits_bmp)
})

# Criar tabelas pivotadas
tempo_compressao_heatmap = tempo_data.pivot_table(
    values="Tempo Compressão (s)",
    index="Tipo de Arquivo",
    columns="Número de Bits",
    aggfunc="mean"
)

tempo_descompressao_heatmap = tempo_data.pivot_table(
    values="Tempo Descompressão (s)",
    index="Tipo de Arquivo",
    columns="Número de Bits",
    aggfunc="mean"
)

# Heatmap: Tempo de Compressão
st.subheader("Heatmap: Tempo de Compressão")
fig4, ax4 = plt.subplots(figsize=(10, 5))
sns.heatmap(tempo_compressao_heatmap, annot=True, fmt=".2f", cmap="Blues", ax=ax4)
ax4.set_title("Tempo de Compressão (s) por Tipo de Arquivo e Número de Bits")
st.pyplot(fig4)

st.markdown("""
O heatmap "Tempo de Compressão" apresenta uma visão clara da relação entre o tipo de arquivo, o número máximo de bits configurados no algoritmo LZW e o tempo de compressão. Ele destaca diferenças significativas entre arquivos de texto (.txt) e de imagem (.bmp), refletindo a complexidade e redundância características de cada tipo de dado.

Para arquivos .txt, o tempo de compressão permanece consistentemente baixo, com valores em torno de 0,02 segundos para todos os tamanhos de dicionário. Isso demonstra a alta eficiência do algoritmo ao lidar com dados de texto, que geralmente possuem padrões mais repetitivos e são processados de forma rápida, mesmo com configurações de dicionários maiores. A ausência de variação significativa no tempo de compressão reforça que o processamento de arquivos de texto não é sensível ao aumento no número máximo de bits.

Por outro lado, para arquivos .bmp, o tempo de compressão varia de forma muito mais pronunciada. Observa-se que, com 9 bits, o tempo é o mais alto, alcançando 8,95 segundos. À medida que o número máximo de bits aumenta, o tempo de compressão diminui de forma consistente, caindo para 1,86 segundos com 16 bits. Esse comportamento indica que, para arquivos de imagem, dicionários maiores permitem representar padrões de maneira mais eficiente, reduzindo a quantidade de operações necessárias durante a compressão.

A comparação entre os dois tipos de arquivo revela que a compressão de imagens é significativamente mais custosa em termos de tempo do que a compressão de texto, especialmente para configurações com dicionários pequenos. No entanto, o impacto do aumento no número máximo de bits é muito mais relevante para imagens, com uma melhoria substancial no tempo de compressão à medida que o tamanho do dicionário cresce.
""")

# Heatmap: Tempo de Descompressão
st.subheader("Heatmap: Tempo de Descompressão")
fig5, ax5 = plt.subplots(figsize=(10, 5))
sns.heatmap(tempo_descompressao_heatmap, annot=True, fmt=".2f", cmap="Greens", ax=ax5)
ax5.set_title("Tempo de Descompressão (s) por Tipo de Arquivo e Número de Bits")
st.pyplot(fig5)

st.markdown("""
O heatmap "Tempo de Descompressão" apresenta a relação entre o tipo de arquivo, o número máximo de bits configurados no algoritmo LZW e o tempo necessário para descompressão. Assim como no tempo de compressão, ele destaca diferenças importantes entre os arquivos de texto (.txt) e de imagem (.bmp), refletindo a complexidade inerente de cada formato.

Para os arquivos .txt, o tempo de descompressão é extremamente baixo e constante, em torno de 0,01 segundos para todos os tamanhos de dicionário (número máximo de bits). Isso demonstra a simplicidade do processo de descompressão para arquivos de texto, que possuem padrões mais previsíveis e são facilmente reconstruídos a partir dos códigos do dicionário, independentemente do tamanho do mesmo. Essa estabilidade no tempo de descompressão reforça a eficiência do algoritmo LZW em lidar com dados textuais.

Já para os arquivos .bmp, o tempo de descompressão é consideravelmente maior, especialmente com dicionários menores. Com 9 bits, o tempo de descompressão é o mais alto, atingindo 7,48 segundos. À medida que o número máximo de bits aumenta, o tempo de descompressão diminui de maneira constante, chegando a 1,33 segundos com 16 bits. Esse comportamento evidencia que, com dicionários maiores, a descompressão se torna mais eficiente, pois as sequências podem ser reconstruídas com menos operações. A redução no tempo é mais pronunciada a partir de 13 bits, indicando que, para imagens, dicionários grandes desempenham um papel fundamental na melhoria do desempenho.

Comparando os tempos de descompressão de .txt e .bmp, fica claro que o processo para arquivos de imagem é muito mais custoso, mesmo nas configurações mais otimizadas. No entanto, a redução no tempo de descompressão para imagens é significativa com o aumento do número de bits, destacando a importância de ajustar o tamanho do dicionário para obter eficiência máxima.
""")


# Conclusão
st.header("Conclusão")
st.markdown("""
O algoritmo LZW provou ser altamente eficiente e versátil em diferentes cenários de compressão, apresentando resultados que variam conforme o tipo de arquivo e a configuração do dicionário. Nos testes realizados, foram avaliados arquivos de texto com tamanho de 74.248 bits e arquivos de imagem bitmap com 2.097.584 bits, considerando versões dinâmica e estática do algoritmo, e o impacto de diferentes números máximos de bits variando entre 9 e 16.

Para arquivos de texto, o LZW atingiu taxas de compressão elevadas, com um máximo de 47,81%, demonstrando alta eficiência em identificar e compactar padrões repetitivos típicos desse formato. Além disso, o tempo de compressão e descompressão foi insignificante, permanecendo estável independentemente do tamanho do dicionário, o que reflete a simplicidade dos padrões encontrados nos textos.

Por outro lado, em arquivos de imagem bitmap, as taxas de compressão foram mais variáveis, alcançando até 59,5% com dicionários maiores. O tempo de compressão e descompressão foi significativamente mais elevado em comparação aos textos, especialmente para configurações com dicionários pequenos. No entanto, observou-se uma redução substancial nos tempos à medida que o número máximo de bits aumentava, indicando que dicionários maiores conseguem otimizar de forma expressiva o desempenho para arquivos de imagem, que possuem padrões mais complexos.

Em suma, o LZW é uma ferramenta poderosa para compressão de dados, mas seu desempenho depende diretamente das características do arquivo e da configuração do dicionário. Futuros trabalhos podem explorar variantes do LZW, como versões adaptativas, para lidar com diferentes tipos de dados e aumentar a eficiência em cenários mais diversos. Além disso, incluir testes com outros formatos de arquivo, como áudio e vídeo, pode expandir ainda mais a aplicabilidade do algoritmo.
""")
