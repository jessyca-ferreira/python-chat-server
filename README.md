# python-chat-server

Isto é uma implementação de um servidor de mensagens em Python, utilizando UDP e (futuramente) o método RDT 3.0

Até o momento, implementamos a transferência de arquivos utilizando sockets UDP.

Para que a transferência funcione, é necessário que ambos os arquivos ```client.py``` e ```server.py``` estejam em estado de execução ao mesmo tempo. Na nossa implementação, a ordem é irrelevante — a conexão entre cliente e servidor será estabelecida, independemente se o primeiro arquivo a ser executado é ```client.py``` ou ```server.py``` **(VER OBSERVAÇÃO 2)**.

Todos os arquivos que serão transferidos para o servidor devem estar localizados na pasta ```client-files```. Deixamos alguns arquivos de exemplo, mas a transferência deve funcionar para qualquer arquivo que seja colocado dentro da pasta posteriormente. Para iniciar o processo de transferência, basta digitar o nome do arquivo, localizado dentro de ```client-files```, no terminal em que ```client.py``` está sendo executado <em>**(ao digitar o nome, a extensão do arquivo deve ser incluida! Exemplo: text não é um arquivo dentro da pasta, mas text.txt é)**</em>.

O arquivo transferido será então salvo em ```server-files``` e, em seguida, retornado ao cliente com um nome modificado (received + nome_original_do_arquivo), conforme sugestão deixada na especificação do projeto.

## Observações e possíveis erros

**1. OBS:** O comando CTRL+X, além de fechar o cliente, fecha também o servidor. Entendemos que esse não é o comportamente usual de uma estrutura cliente-servidor, mas seguimos o tutorial postado no classroom da disciplina, onde é sugerido esse método, já que sem isso o servidor poderia ser encerrado somente pelo gerenciador de tarefas, tornando os processos de teste e correção mais lentos.

**2. OBS:** Reforçamos que é necessário que os arquivos que serão enviados estejam em ```client-files```, e que ```client-files``` esteja localizado no mesmo diretório dos arquivos ```client.py``` e ```server.py```. Além disso, é importante que a pasta aberta na IDE ou editor de código seja a pasta onde os arquivos .py estão localizados. Caso contrário, receberá um erro parecido com o da imagem abaixo, ou não conseguirá executar o cliente.

![image](https://github.com/jessyca-ferreira/python-chat-server/assets/133786404/1389a84b-ebff-4591-901c-5f234d283ff4)
  
**NÃO** abra o diretório dessa forma:

![image](https://github.com/jessyca-ferreira/python-chat-server/assets/133786404/3d7b897c-c09a-4195-8d9e-660e0e6b59f6)

**ABRA** o diretório dessa forma:

![image](https://github.com/jessyca-ferreira/python-chat-server/assets/133786404/0c50a840-634b-467d-b7b9-7c72dc595638)



## Equipe 4

Beatriz de Oliveira Barros - bob@cin.ufpe.br

Jessyca Ferreira da Silva -	jfs7@cin.ufpe.br

Letícia Barbosa Lins Pedrosa - lblp@cin.ufpe.br

Maike Henrique Rodrigues de Menezes	- mhrm2@cin.ufpe.br

Paulo Rafael Barros de Aguiar	- prba@cin.ufpe.br

Pedro Martins da Silva - pms5@cin.ufpe.br
