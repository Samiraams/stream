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
O algoritmo LZW provou ser altamente eficiente e versátil em diferentes cenários de compressão, apresentando resultados que variam conforme o tipo de arquivo e a configuração do dicionário. Nos testes realizados, foram avaliados arquivos de texto com tamanho de 74.248 bits e arquivos de imagem bitmap com 2.097.584 bits, considerando versões dinâmica e estática do algoritmo, e o impacto de diferentes números máximos de bits variando entre 9 e 16.

Para arquivos de texto, o LZW atingiu taxas de compressão elevadas, com um máximo de 47,81%, demonstrando alta eficiência em identificar e compactar padrões repetitivos típicos desse formato. Além disso, o tempo de compressão e descompressão foi insignificante, permanecendo estável independentemente do tamanho do dicionário, o que reflete a simplicidade dos padrões encontrados nos textos.

Por outro lado, em arquivos de imagem bitmap, as taxas de compressão foram mais variáveis, alcançando até 59,5% com dicionários maiores. O tempo de compressão e descompressão foi significativamente mais elevado em comparação aos textos, especialmente para configurações com dicionários pequenos. No entanto, observou-se uma redução substancial nos tempos à medida que o número máximo de bits aumentava, indicando que dicionários maiores conseguem otimizar de forma expressiva o desempenho para arquivos de imagem, que possuem padrões mais complexos.

Em suma, o LZW é uma ferramenta poderosa para compressão de dados, mas seu desempenho depende diretamente das características do arquivo e da configuração do dicionário. Futuros trabalhos podem explorar variantes do LZW, como versões adaptativas, para lidar com diferentes tipos de dados e aumentar a eficiência em cenários mais diversos. Além disso, incluir testes com outros formatos de arquivo, como áudio e vídeo, pode expandir ainda mais a aplicabilidade do algoritmo.
""")
