import {
    UseMutationOptions,
    DefaultOptions,
    QueryClient,
} from '@tanstack/react-query';

export type QueryConfig<T extends (...args: any[]) => any> = Omit<
    ReturnType<T>,
    'queryKey' | 'queryFn'
>;

export type ApiFnReturnType<FnType extends (...args: any) => Promise<any>> =
    Awaited<ReturnType<FnType>>;

export type MutationConfig<
    MutationFnType extends (...args: any) => Promise<any>,
> = UseMutationOptions<
    ApiFnReturnType<MutationFnType>,
    Error,
    Parameters<MutationFnType>[0]
>;
