function crowding_distance = calculateCrowdingDistance(population, F)
    [N, M] = size(F);
    crowding_distance = zeros(N, 1);
    for m = 1:M
        [~, index] = sort(F(:, m));
        crowding_distance(index(1)) = 1;
        crowding_distance(index(N)) = 1;
        for i = 2:N-1
            if ~isinf(crowding_distance(index(i)))
                crowding_distance(index(i)) = crowding_distance(index(i)) + (F(index(i+1), m) - F(index(i-1), m))/(max(F(:, m)) - min(F(:, m)));
            end
        end
    end
end
