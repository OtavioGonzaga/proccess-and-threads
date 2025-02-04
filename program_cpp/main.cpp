#include <iostream>
#include <vector>
#include <chrono>
#include <omp.h>
#include <tbb/tbb.h>

int main()
{
	const int N = 100000000;
	std::vector<int> vetor(N, 1);

	// Cálculo sequencial
	int resultado_sequencial = 0;
	auto inicio_sequencial = std::chrono::high_resolution_clock::now();
	for (int i = 0; i < N; i++)
	{
		resultado_sequencial += vetor[i];
	}
	auto fim_sequencial = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> duracao_sequencial = fim_sequencial - inicio_sequencial;

	// Cálculo paralelo com OpenMP
	int resultado_paralelo_omp = 0;
	auto inicio_paralela_omp = std::chrono::high_resolution_clock::now();
	#pragma omp parallel for reduction(+ : resultado_paralelo_omp)
	for (int i = 0; i < N; ++i)
	{
		resultado_paralelo_omp += vetor[i];
	}
	auto fim_paralela_omp = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> duracao_paralela_omp = fim_paralela_omp - inicio_paralela_omp;

	// Cálculo paralelo com Intel TBB
	auto inicio_paralela_tbb = std::chrono::high_resolution_clock::now();
	int resultado_paralelo_tbb = tbb::parallel_reduce(
		tbb::blocked_range<int>(0, N), 0,
		[&](const tbb::blocked_range<int> &r, int soma_thread) -> int
		{
			for (int i = r.begin(); i < r.end(); ++i)
				soma_thread += vetor[i];
			return soma_thread;
		},
		std::plus<int>());
	auto fim_paralela_tbb = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> duracao_paralela_tbb = fim_paralela_tbb - inicio_paralela_tbb;

	// Saída dos resultados
	std::cout << "Tempo sequencial: " << duracao_sequencial.count() << " segundos." << std::endl;
	std::cout << "Tempo TBB: " << duracao_paralela_tbb.count() << " segundos." << std::endl;
	std::cout << "Tempo OpenMP: " << duracao_paralela_omp.count() << " segundos." << std::endl;

	return 0;
}
