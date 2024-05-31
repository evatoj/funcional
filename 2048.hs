import Data.Char (toLower)
import Data.List (concat, transpose)
import System.IO (BufferMode (NoBuffering), hSetBuffering, stdin)
import System.Random (randomRIO)
import Text.Printf (printf)

data Movimento = Cima | Baixo | Esquerda | Direita

type Grade = [[Int]]

iniciar :: IO Grade
iniciar = adicionar2ou4 =<< adicionar2ou4 (replicate 4 [0, 0, 0, 0])

juntar :: [Int] -> [Int]
juntar xs = unido ++ replicate (length xs - length unido) 0
  where
    unido = combinar $ filter (/= 0) xs
    combinar (x : y : rest)
      | x == y = x * 2 : combinar rest
      | otherwise = x : combinar (y : rest)
    combinar rest = rest

mover :: Movimento -> Grade -> Grade
mover Esquerda = map juntar
mover Direita = map (reverse . juntar . reverse)
mover Cima = transpose . mover Esquerda . transpose
mover Baixo = transpose . mover Direita . transpose

vazio :: Grade -> [(Int, Int)]
vazio grade = [(linha, coluna) | linha <- [0 .. 3], coluna <- [0 .. 3], grade !! linha !! coluna == 0]

verificarMovimento :: Grade -> Bool
verificarMovimento grade = any (/= grade) [mover m grade | m <- [Esquerda, Direita, Cima, Baixo]]

imprimirGrade :: Grade -> IO ()
imprimirGrade grade = do
  putStr "\ESC[2J\ESC[2J\n"
  mapM_ (putStrLn . concatMap (printf "%5d")) grade

pecas :: [(Char, Movimento)]
pecas = zip "wasdchtn" [Cima, Esquerda, Baixo, Direita, Cima, Esquerda, Baixo, Direita]

jogada :: IO Movimento
jogada = do
  entrada <- getChar
  maybe jogada return (lookup (toLower entrada) pecas)

verificar2048 :: Grade -> Bool
verificar2048 = elem 2048 . concat

adicionar2ou4 :: Grade -> IO Grade
adicionar2ou4 grade = do
  escolha <- escolher (vazio grade)
  definirQuadrado grade escolha <$> escolher [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]

escolher :: [a] -> IO a
escolher xs = (xs !!) <$> randomRIO (0, length xs - 1)

definirQuadrado :: Grade -> (Int, Int) -> Int -> Grade
definirQuadrado grade (linha, coluna) val =
  let (pre, resto) = splitAt linha grade
      (meio, pos) = splitAt coluna (head resto)
   in pre ++ [meio ++ val : tail pos] ++ tail resto

novaGrade :: Grade -> IO Grade
novaGrade grade = mover <$> jogada <*> return grade

loopJogo :: Grade -> IO ()
loopJogo grade
  | verificarMovimento grade = do
      imprimirGrade grade
      if verificar2048 grade
        then putStrLn "Venceu :)"
        else do
          nova_grade <- novaGrade grade
          if grade /= nova_grade
            then loopJogo =<< adicionar2ou4 nova_grade
            else loopJogo grade
  | otherwise = imprimirGrade grade >> putStrLn "Perdeu :("

main :: IO ()
main = do
  hSetBuffering stdin NoBuffering
  grade <- iniciar
  loopJogo grade