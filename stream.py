import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 

# Título e Introdução
st.title("Compressão e Descompressão de Arquivos com LZW")
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
            
O **algoritmo LZW (Lempel-Ziv-Welch)** é uma técnica de compressão sem perdas que substitui padrões repetidos nos dados por códigos inteiros exclusivos. Ele constrói um dicionário que mapeia sequências de entrada para códigos, permitindo uma representação mais compacta dos dados sem perda de informação.

#### 1. Compressão Estática (`lzw_encoder`)

Na compressão estática, o tamanho dos códigos é fixo, determinado pelo parâmetro `bits_max`, que define o número máximo de bits para representar cada código. O processo começa inicializando um dicionário com todas as sequências de um único byte (256 entradas correspondentes aos códigos ASCII). Conforme os dados são lidos, o algoritmo forma sequências e verifica se elas já existem no dicionário:

- **Se a sequência existe**, continua adicionando bytes para formar uma sequência maior.
- **Se a sequência não existe**:
  - Emite o código da sequência anterior.
  - Adiciona a nova sequência ao dicionário (se o limite não foi atingido).
  - Reinicia a construção da sequência com o byte atual.

#### 2. Descompressão Estática (`lzw_decoder`)

A descompressão estática reverte o processo de compressão usando o mesmo tamanho fixo de códigos. O dicionário é inicializado da mesma forma e reconstruído à medida que os códigos são lidos:

- Lê cada código do arquivo compactado.
- Converte o código na sequência correspondente usando o dicionário.
- Adiciona novas sequências ao dicionário, combinando sequências anteriores com novos bytes.
- Reconstrói os dados originais emitindo as sequências decodificadas.

#### 3. Compressão Dinâmica (`lzw_encoder_variable`)

Na compressão dinâmica, o tamanho dos códigos pode aumentar conforme o dicionário cresce, começando geralmente com 9 bits e podendo chegar até o limite definido por `bits_max`. O algoritmo ajusta dinamicamente o número de bits necessários para representar os códigos:

- Inicia com um dicionário básico, como na versão estática.
- Conforme novas sequências são adicionadas e o número de entradas excede o que pode ser representado com o número atual de bits, incrementa o tamanho dos códigos em um bit.
- Isso permite que o dicionário cresça e capture padrões mais complexos, potencialmente melhorando a taxa de compressão em arquivos maiores.

#### 4. Descompressão Dinâmica (`lzw_decoder_variable`)

A descompressão dinâmica acompanha as mudanças no tamanho dos códigos feitas durante a compressão:

- Inicia com o mesmo dicionário básico.
- Lê os códigos do arquivo compactado, ajustando o número de bits conforme necessário.
- Reconstrói as sequências originais usando o dicionário atualizado.
- Adiciona novas sequências ao dicionário e incrementa o tamanho dos códigos em sincronia com o processo de compressão.
            
#### 5. Decisão de Implementação para Descompressões
            
Optamos por escrever no header dos arquivos comprimidos informações para guiar a descompressão mais facilmente. Os dados armazenados foram: a extensão do arquivo original, o tipo de compressão (fixo ou variável) e o tamanho máximo dos bits usados.

#### 6. Manipulação de Bits

Para lidar com tamanhos de códigos variáveis, fizemos uso de métodos auxiliares:

- **Bit_writer**: Escreve os códigos no arquivo compactado, garantindo que cada código use exatamente o número correto de bits e que os bits sejam alinhados corretamente no fluxo de saída.
- **Bit_reader**: Lê os códigos do arquivo compactado, interpretando corretamente a quantidade de bits que compõe cada código, especialmente quando o tamanho dos códigos muda dinamicamente.

#### Benefícios e Limitações

Ambos algoritmos tem um comportamento melhor para dados que são mais redundantes, ou seja, que sejam mais fáceis de identificar padrões. No caso da versão estática, temos uma implementação mais simples que a segunda, e um uso mais consistente de memória, porém o tamanho fixo do dicionário pode limitar a eficiência em arquivos com muitos padrões únicos ou complexos. Para a versão dinâmica/variável, temos uma melhor adaptação ao conteúdo dos dados, potencialmente melhorando a taxa de compressão por conseguir capturar padrões mais longos e complexos, mas sua implementação é mais complexa e tem um maior uso de memória.

---
""")

# Análises e Resultados
st.header("Análises e Resultados")

st.markdown("""

Primeiramente, nosso objetivo foi avaliar o comportamento de ambas versões do algoritmo para diferentes tipos de arquivos.
Os tipos considerados nas análises subsequentes foram: txt, bmp, csv e pdf. Escolhemos esses dois formatos adicionais por
serem de utilidade frequente no nosso dia a dia, e gostaríamos de avaliar o quanto o método implementado seria efetivo.
            
Para explorar os resultados obtidos, vamos apresentá-los em duas etapas: primeiramente no aspecto da compressão e, em seguida,
avaliando a descompressão desses arquivos. Todas as métricas seguintes foram feitas com base na média obtida de três execuções
com arquivos distintos.

### Compressão
        
""")

st.markdown("""

O gráfico abaixo apresenta o comportamento da taxa de compressão em relação ao número máximo de bits utilizado. Podemos verificar que, no geral, a versão variável do algoritmo teve um desempenho melhor quando comparamos com a versão fixa. No caso da versão fixa, vemos que ela apresenta uma taxa de compressão relativamente estável para a maioria dos arquivos a partir de 12 bits, enquanto a versão variável exibe um crescimento mais pronunciado nas taxas de compressão à medida que os bits aumentam. Arquivos como bmp e csv obtêm maior benefício do aumento do tamanho do dicionário na versão variável. É importante notar o quanto o algoritmo em nenhuma de suas versões foi efetivo para arquivos pdf, uma vez que ao comprimir ele acabou por aumentar o tamanho do arquivo. Isso ocorre porque arquivos pdf já são otimizados no sentido de compressão, uma vez que ele deve armazenar textos e figuras de maneira eficiente, além de que muito possívelmente o algoritmo não foi capaz de identificar muitos padrões para reduzi-lo. Em contrapartida, vemos que arquivos csv que são muito utilizados para manipulação de dados, por exemplo, foi de maneira consistente o de melhor taxa de compressão para a versão variável do LZW.

""")

st.image("images/compression_rate_vs_bits.png", caption="", use_column_width=True)

st.markdown("""

Na próxima visualização estão dispostas as variações da razão de compressão pelo número de bits máximos. Arquivos com alta redundância, como TXT e CSV, apresentam as maiores razões de compressão, alcançando um resultado melhor em ambas as estratégias, com uma leve vantagem para a compressão variável, que utiliza dicionários maiores para capturar padrões mais complexos. Já arquivos mais complexos, como PDFs e BMPs, apresentam razões de compressão mais baixas, principalmente na compressão fixa, devido à limitação no tamanho do dicionário. Na compressão variável, observa-se uma melhoria significativa na razão de compressão para esses arquivos a partir de 13 bits, mostrando que padrões complexos podem ser melhor representados com dicionários dinâmicos.

""")

st.image("images/compression_ratio_vs_bits.png", caption="", use_column_width=True)

st.markdown("""

Para o gráfico seguite, temos o crescimento do dicionário utilizado na compressão entre os diferentes tipos de arquivos. Primeiramente, vamos avaliar o comportamento para a sua versão fixa. Observando o gráfico, vemos o quanto arquivos pdf tiveram mais entradas em relação aos demais tipos de arquivos uma vez que, como dito anteriormente, arquivos pdf podem ter estruturas com padrões mais difíceis de serem identificado, isso se tiverem algum padrão. Além disso, arquivos BMP também apresentam um crescimento acentuado com o crescimento do tamanho de bits, o que pode ter acontecido também devido à baixa redundância nos dados da imagem, o que leva o algoritmo a criar novas entradas para representar os padrões. Quanto aos arquivos csv e txt é possível verificar também um crescimento das entradas, porém muito mais reduzido em relação aos anteriores.

""")

# st.image("images/compression_rate_vs_time_fixed.png", caption="", use_column_width=True)
# st.image("images/compression_rate_vs_time_variable.png", caption="", use_column_width=True)
st.image("images/dictionary_growth_fixed.png", caption="", use_column_width=True)

st.markdown("""

Agora, avaliando o crescimento do dicionário no algoritmo variável, vemos que o número de entradas no dicionário para arquivos pdf é ainda superior em relação a versão fixa do algoritmo. Quanto a arquivos BMP, vemos que para valores maiores de comprimento dos bits seu número de entradas é reduzido. Quanto a arquivos csv e txt temos uma concentração maior para 10000 entradas, sendo um pouco inferior a esse valor para valores máximos de 11, 12 e 13.

""")

st.image("images/dictionary_growth_variable.png", caption="", use_column_width=True)

st.markdown("""

O gráfico seguinte exibe os valores de tempo de execução médio para a compressão desses diferentes tipos de arquivos. O arquivo pdf possui um tempo de execução maior em relação aos demais, muito associado a quantidade de entradas no dicionário que ele deve gerar para identificação de padrões no texto. Para a versão variável em txt e csv, o tempo de execução é maior para configurações de bits menores (9-11 bits) e reduz gradualmente à medida que o número de bits aumenta. Quanto a arquivos BMP, eles também possuem tempos de execução maiores com dicionários pequenos na versão variável, que diminuem conforme o número de bits cresce. Isso indica que o bmp, sendo um formato de imagem, possui padrões mais difíceis de capturar com dicionários pequenos. Para os arquivos txt e csv, os tempos de execução são consistentemente baixos em ambas as versões do algoritmo, com pouca variação conforme o número máximo de bits aumenta.

""")

st.image("images/execution_time_vs_bits.png", caption="", use_column_width=True)

st.markdown("""

Para finalizar os resultados referentes à compressão desses arquivos, abaixo está disposto um mapa de calor indicando a taxa de compressão para os tipos de arquivos em função do número máximo de bits configurados e da versão do algoritmo LZW.  Arquivos como bmp e csv se beneficiam significativamente de dicionários maiores, especialmente na versão variável, que adapta o tamanho progressivamente, atingindo taxas de compressão superiores a 30%. Em contraste, arquivos pdf, devido à sua complexidade e ao fato de frequentemente conterem dados já comprimidos, resultam em taxas negativas (expansão) em ambas as versões do algoritmo, reforçando a inadequação do LZW para esse formato. Para arquivos txt, a redundância estrutural permite compressões moderadas na versão fixa (~16%) e superiores na versão variável (~25%), mesmo com dicionários pequenos.

""")

st.image("images/heatmap_compression_rate.png", caption="", use_column_width=True)

st.markdown("### Descompressão")

st.markdown("""

No gráfico a seguir temos o crescimento do dicionário na etapa de descompressão. A maioria dos arquivos comprimidos usando uma estratégia de compressão fixa apresenta um dicionário que atinge um tamanho estável, mesmo com o aumento do número máximo de bits, exceto para o caso do pdf, cujo dicionário cresce significativamente com o aumento dos bits máximos. Para o método variável, houve um comportamento mais dinâmico, com o tamanho do dicionário variando de acordo com o número de bits máximos permitidos. No BMP, por exemplo, cresce rapidamente com tamanhos maiores de bits máximos.

""")

st.image("images/decompression_dictionary_growth.png", caption="", use_column_width=True)

st.markdown("""

Quanto ao tempo de execução da descompressão, é possível verificar que seu comportamento também foi semelhante ao comportamento no gráfico de compressão, exceto pelo fato de que o tempo de execução na descompressão é um pouco menor em relação à compressão. O tempo de execução para a descompressão de arquivos com compressão fixa permanece estável e consistentemente baixo para todos os tipos de arquivos. Isso ocorre porque o tamanho do dicionário é limitado e não cresce dinamicamente durante o processo. Qunato ao variável, eles apresentam maior variação no tempo de execução da descompressão. O tempo tende a ser maior inicialmente, especialmente para tipos de arquivos como PDF e BMP, mas diminui progressivamente à medida que o número de bits máximos aumenta.

""")

st.image("images/decompression_execution_time.png", caption="", use_column_width=True)

st.markdown("""

Abaixo, vemos o comportamento do uso da memória na descompressão. O gráfico evidencia como a estratégia de compressão (fixa ou variável) e o tipo de arquivo influenciam o uso de memória durante a descompressão. Na versão fixa, o uso de memória permanece baixo e constante para todos os tipos de arquivo, devido ao tamanho limitado do dicionário, garantindo estabilidade e previsibilidade. Por outro lado, na compressão variável, o uso de memória varia significativamente, especialmente para arquivos mais complexos como PDFs e BMPs, onde há um aumento expressivo à medida que os bits máximos crescem, refletindo a necessidade de dicionários maiores para representar padrões complexos. Os arquivos txt mostram um comportamento inverso na compressão variável, com um uso inicial elevado de memória que diminui conforme os bits máximos aumentam, indicando maior eficiência na compactação de padrões. Quanto a arquivos csv, eles apresentam baixo uso de memória em ambas as estratégias. Esses resultados mostram que a compressão variável pode ser mais custosa em termos de memória para arquivos complexos, enquanto a compressão fixa oferece maior controle e eficiência no uso de recursos.

""")

st.image("images/memory_usage_decompression.png", caption="", use_column_width=True)

# Conclusão
st.header("Conclusão")
st.markdown("""
            
Após a realização das análises, concluímos que o algoritmo LZW, em suas versões estática e dinâmica, apresenta desempenhos variados dependendo do tipo de arquivo e dos parâmetros configurados. A compressão para os dois métodos demonstrou maior eficiência em arquivos com alta redundância, como os arquivos txt e csv, porém a versão variável alcançou taxas de compressão superiores quando comparada à versão estática. No entanto, para arquivos como PDF, que já possuem algum nível de compressão ou possuem padrões menos evidentes, ambas as versões não foram eficazes, resultando até mesmo no aumento do tamanho do arquivo após a compressão.

Observamos também que o número máximo de bits é um fator crucial que influencia diretamente o desempenho dos algoritmos. Na compressão dinâmica, o aumento do número de bits permitiu um crescimento do dicionário, capturando sequências mais longas e aprimorando a taxa de compressão. Entretanto, isso também acarretou em um maior uso de memória e tempo de processamento, especialmente em arquivos complexos. Por outro lado, a compressão estática, com seu tamanho de dicionário fixo, proporcionou um uso de recursos mais consistente, embora com taxas de compressão inferiores em certos casos.

Em suma, a escolha entre a compressão estática e dinâmica deve levar em consideração o tipo de arquivo e os recursos computacionais disponíveis. A compressão dinâmica é recomendada para arquivos grandes e com muitos padrões repetitivos, enquanto a compressão estática pode ser mais adequada para arquivos menores ou quando há limitações de memória e processamento. Existem melhorias que podem ser implementadas para aumentar a taxa de compressão dos arquivos, pois mesmo que tenham tido certa redução, não tiveram valores tão marcantes quanto seria desejado em um uso prático, por exemplo.
                                   
""")